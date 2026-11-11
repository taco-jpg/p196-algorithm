#!/usr/bin/env python3
"""r13a driver: one L or R instance.
L: python bandrun.py L --b 10 --clock 1000 --V 18,9,0 --T 120 --tau 0 --rot 0 --R 12 --solver kissat404 [--g G] [--nofor] [--notrim] [--epochs M]
R: python bandrun.py R --b 10 --clock 1000 --V 18,9,0 --T 120 --tau 0 --rot 0 --Rfree 20 --solver kissat404 [--epochs M] [--nofor] [--delta D]
T = band period (multiple of clock period); tau = time origin (row V_tau, clock phase tau); rot = rotation applied to V_tau.
Epochs M: instance over M*T steps (final condition after M*T steps)."""
import sys, time, argparse, resource
import bandsat as BS
import bandsat2 as BS2


def setup(a):
    b = a.b
    V = [int(x) for x in a.V.split(',')]
    clk = [int(ch) for ch in a.clock]
    p = len(clk)
    T = a.T
    # V is the band word at clock phase 0 (time 0); rows V_0..V_T
    def clock(t):
        return clk[t % p]
    rows = [list(V)]
    for t in range(T + a.tau):
        y, _, _, _, _ = BS.rowstep(rows[-1], clock(t), b)
        rows.append(y)
    assert rows[T] == list(V), ('V not T-periodic', V, rows[T])
    Vt = rows[a.tau]
    n = len(V)
    W = Vt[a.rot:] + Vt[:a.rot]
    TT = a.Tprime if a.Tprime else a.epochs * T
    cl = [clock(a.tau + t) for t in range(TT)]
    return b, W, cl, TT, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode')
    ap.add_argument('--b', type=int, default=10)
    ap.add_argument('--clock', required=True)
    ap.add_argument('--V', required=True)
    ap.add_argument('--T', type=int, required=True)
    ap.add_argument('--tau', type=int, default=0)
    ap.add_argument('--rot', type=int, default=0)
    ap.add_argument('--epochs', type=int, default=1)
    ap.add_argument('--R', type=int, default=12)
    ap.add_argument('--Rfree', type=int, default=0)
    ap.add_argument('--g', type=int, default=0)
    ap.add_argument('--nofor', action='store_true')
    ap.add_argument('--notrim', action='store_true')
    ap.add_argument('--solver', default='kissat404')
    ap.add_argument('--delta', type=int, default=None)
    ap.add_argument('--tag', default='')
    ap.add_argument('--enc', type=int, default=1)
    ap.add_argument('--allepochs', action='store_true', help='L*(M): band correct at every epoch boundary j*T, j=1..M')
    ap.add_argument('--Tprime', type=int, default=0, help='override the total number of steps T\' (e.g. T_rot for an epoch of a twisted band; rows at that time must be a rotation of the starting word)')
    ap.add_argument('--markevery', type=int, default=0, help='extra band-correct marks at all multiples of this many steps (e.g. T_rot); implies intermediate conditions')
    ap.add_argument('--comoving', action='store_true', help='R*: comoving return of the free cells')
    ap.add_argument('--ret', action='store_true', help='D-type: free columns return exactly at the end (exact-period junction)')
    a = ap.parse_args()
    t0 = time.time()
    b, W, cl, TT, n = setup(a)
    tag = f'{a.mode}{"D" if a.ret else ""}{"*" if a.allepochs or a.comoving or a.markevery else ""} b={b} clock={a.clock} V={a.V} T={a.T} epochs={a.epochs} Tprime={a.Tprime or a.epochs*a.T} tau={a.tau} rot={a.rot} word={W} solver={a.solver} trim={not a.notrim and a.enc==1} enc={a.enc}'
    if a.mode == 'L':
        marks = None
        if a.markevery:
            marks = [j * a.markevery for j in range(1, TT // a.markevery + 1) if j * a.markevery < TT]
        elif a.allepochs:
            marks = [j * a.T for j in range(1, a.epochs)]
        if a.enc == 1:
            E, X, AL, BE, HL, info = BS.build_L(b, W, cl, a.R, g_final=a.g, foreign=not a.nofor, trim=not a.notrim, solver=a.solver, epoch_marks=marks, require_period=not a.Tprime, ret_free=a.ret)
        else:
            E, X, AL, BE, HL, info = BS2.build_L2(b, W, cl, a.R, g_final=a.g, foreign=not a.nofor, solver=a.solver, epoch_marks=marks, require_period=not a.Tprime)
        tag += f' R={a.R} g={a.g} nofor={int(a.nofor)} W={info["W"]} front={info["front"]}'
        tb = time.time() - t0
        r = E.S.solve()
        ans = 'SAT' if r else 'UNSAT'
        extra = ''
        if r:
            m = set(l for l in E.S.get_model() if l > 0)
            f = BS.letter_of(m, X[0][a.R - 1])
            free0 = [BS.letter_of(m, X[0][c])[0] for c in range(a.R)]
            extra = f' foreign_letter={f} leftcols0={free0}'
        print(f'RESULT {tag} : {ans}{extra} vars={E.nv} clauses={E.nc} build={tb:.1f}s total={time.time()-t0:.1f}s rss={BS.rss_gb():.2f}GB', flush=True)
    elif a.mode == 'R':
        S = sum(cl)
        delta = a.delta
        if delta is None:
            if S % 2:
                print(f'NOTE overflows per epoch S={S} odd; use --epochs 2', flush=True)
                return
            delta = S // 2
        Rfree = a.Rfree if a.Rfree else max(a.R, delta + n)
        if a.enc == 1:
            E, X, AL, BE, HL, info = BS.build_R(b, W, cl, Rfree=Rfree, delta=delta, foreign=not a.nofor, trim=not a.notrim, solver=a.solver, comoving=a.comoving)
        else:
            E, X, AL, BE, HL, info = BS2.build_R2(b, W, cl, Rfree=Rfree, delta=delta, foreign=not a.nofor, solver=a.solver, comoving=a.comoving)
        tag += f' Rfree={Rfree} delta={delta} S={S} nofor={int(a.nofor)} front={info["front"]} Z={info["Z"]}'
        tb = time.time() - t0
        r = E.S.solve()
        ans = 'SAT' if r else 'UNSAT'
        extra = ''
        if r:
            m = set(l for l in E.S.get_model() if l > 0)
            f = BS.letter_of(m, X[0][info['Z']])
            extra = f' foreign_letter={f}'
        print(f'RESULT {tag} : {ans}{extra} vars={E.nv} clauses={E.nc} build={tb:.1f}s total={time.time()-t0:.1f}s rss={BS.rss_gb():.2f}GB', flush=True)
    else:
        raise SystemExit('bad mode')


if __name__ == '__main__':
    main()
