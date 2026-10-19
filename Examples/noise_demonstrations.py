"""Reproducible classroom noise experiments. Requires only NumPy.
Run: python noise_demonstrations.py
CSV figures and numerical_results.txt are saved beside this file.
The RC recursion is the exact sampled stationary Ornstein-Uhlenbeck model.
"""
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(6020)
k, T, C = 1.380649e-23, 290.0, 1e-12
R = 1e3
sigma2 = k*T/C
trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
lines = []
def report(text):
    print(text)
    lines.append(text)
def save(name, data, header):
    np.savetxt(OUT/name, data, header=header, comments="", delimiter=" ")

N = 200000
persistent = np.full(N, rng.choice([-1.,1.]))
independent = rng.choice([-1.,1.], N)
alternating = (-1.)**np.arange(N)
for name, x in [("persistent",persistent),("independent",independent),("alternating",alternating)]:
    y = (x[1:]+x[:-1])/2
    # Ensemble variance of persistent is 1; a single constant record's time variance is 0.
    report(f"FIR {name}: time mean square {np.mean(y*y):.6f}; single-record centered variance {np.var(y):.6f}")

M, n = 64, 16384
dt = R*C/20
a = np.exp(-dt/(R*C))
x = np.empty((M,n))
x[:,0] = rng.normal(0,np.sqrt(sigma2),M)
innovation = rng.normal(0,np.sqrt(sigma2*(1-a*a)),(M,n-1))
for j in range(1,n):
    x[:,j] = a*x[:,j-1]+innovation[:,j-1]
emp = np.mean(x*x)
report(f"RC ensemble mean square / (kT/C): {emp/sigma2:.6f}")
report(f"RC exact RMS: {np.sqrt(sigma2)*1e6:.6f} uV")
lag = np.arange(81)
corr = np.array([np.mean(x[:,:n-int(j)]*x[:,int(j):])/sigma2 for j in lag])
save("rc_correlation.dat", np.column_stack([lag*dt/(R*C),corr,a**lag]),"lag measured theory")
save("rc_waveforms.dat", np.column_stack([np.arange(300)*dt/(R*C), x[:3,:300].T/np.sqrt(sigma2)]),"time x1 x2 x3")
# One fixed time over many independent outcomes: sample many stationary experiments.
hsamples = rng.normal(0,1,50000)
hist, edges = np.histogram(hsamples,bins=np.linspace(-4,4,41),density=True)
centers = (edges[1:]+edges[:-1])/2
save("rc_histogram.dat",np.column_stack([centers,hist,np.exp(-centers**2/2)/np.sqrt(2*np.pi)]),"voltage measured theory")
f = np.fft.rfftfreq(n,dt)
P = np.mean(dt/n * np.abs(np.fft.rfft(x,axis=1))**2,axis=0)
P[1:-1] *= 2
# Rectangle bin sum, not trapezoid, handles once-counted FFT endpoints correctly.
psd_area = np.sum(P)*(f[1]-f[0])
assert np.isclose(psd_area,emp,rtol=1e-12), "FFT normalization violates Parseval"
report(f"FFT bin-sum area / measured mean square: {psd_area/emp:.12f}")
# Log-bin averages for a readable figure, avoiding the DC/Nyquist endpoints.
groups = np.unique(np.geomspace(1,len(f)-1,100).astype(int))
rows=[]
for lo,hi in zip(groups[:-1],groups[1:]):
    fc = np.mean(f[lo:hi]); pm=np.mean(P[lo:hi])
    theory=2*dt*sigma2*(1-a*a)/(1+a*a-2*a*np.cos(2*np.pi*fc*dt))
    continuous=4*k*T*R/(1+(2*np.pi*fc*R*C)**2)
    rows.append([fc*R*C,pm/(4*k*T*R),theory/(4*k*T*R),continuous/(4*k*T*R)])
save("rc_psd.dat",rows,"frequency measured sampled continuous")

# Integrals with u=f/fp, upper cutoff 1e5 and fine logarithmic grid.
u=np.concatenate(([0.],np.geomspace(1e-8,1e5,200000)))
for rr in [1e3,1e4]:
    fp=1/(2*np.pi*rr*C)
    area=trap(4*k*T*rr/(1+u*u),u*fp)
    exact_fraction=2/np.pi*np.arctan(u[-1])
    report(f"R={rr:g} ohm: integral/(kT/C)={area/sigma2:.9f}; finite-limit exact={exact_fraction:.9f}")
    assert np.isclose(area/sigma2,exact_fraction,rtol=1e-7)
for name,response,exact in [
    ("one pole",1/(1+u*u),np.pi/2),
    ("two poles",1/((1+u*u)*(1+(u/4)**2)),np.pi/2*4/5),
    ("two poles + zero",(1+(u/2)**2)/((1+u*u)*(1+(u/4)**2)),np.pi/2*4/5*2)]:
    area=trap(response,u)
    report(f"{name}: ENBW/fp1={area:.8f}; infinite-band exact={exact:.8f}")
    assert abs(area-exact)/exact<2e-5

Fmin=10**(2.16/10)
F50=Fmin+35/.020*abs(.020-(.0085-1j*.0158))**2
report(f"Rounded 60 GHz parameters: NF at 50 ohm={10*np.log10(F50):.6f} dB")
Fs=10**(np.array([1.5,5,12,15])/10)
Gs=10**(np.array([-1.5,18,0])/10)
contributions=np.r_[Fs[0],(Fs[1:]-1)/np.cumprod(Gs)]
Ftot=np.sum(contributions)
report(f"Friis contributions: {contributions}")
report(f"Receiver NF={10*np.log10(Ftot):.6f} dB; Te={290*(Ftot-1):.3f} K")
Gs[1]=10
Flow=Fs[0]+np.sum((Fs[1:]-1)/np.cumprod(Gs))
report(f"With 10 dB LNA gain: NF={10*np.log10(Flow):.6f} dB")
report("Monte Carlo values have finite-record uncertainty; analytic integrals and FFT normalization were checked.")
(OUT/"numerical_results.txt").write_text("\n".join(lines)+"\n")
