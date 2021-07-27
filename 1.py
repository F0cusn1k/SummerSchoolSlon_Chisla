import math

def f(alpha, base):
    r = int(alpha*base)*alpha
    c = False
    if r > 1:
        c = True
        r /= base
    return r, c

def floateq(f1, f2, eps):
    return f1 - f2 < eps and f1 - f2 > -eps

def main():
    while(True):
        base = int(input())
        points = [(1, 0)]
        tau = int(math.log(base)) + 1
        eps = 10**(-tau - 2)

        for k in range(1, base):
            a, c1 = f(k/base, base)
            a = round(a, tau)
            b, c2 = f((k+1-eps)/base, base)
            b = round(b, tau)
            points.append((a, 1))
            points.append((b, -1))
            if c2 and not c1:
                points.append((1, -1))
                points.append((round(1/base, tau), 1))

        points.sort(key = lambda x: x[0])
        segments = []
        ctr = 0

        for i in range(len(points)-1):
            ctr += points[i][1]
            if not floateq(points[i][0], points[i+1][0], eps):
                if len(segments) > 0 and ctr == segments[-1][0]:
                    _, a, _ = segments.pop()
                    segments.append((ctr, a, points[i+1][0]))
                else:
                    segments.append((ctr, points[i][0], points[i+1][0]))
                    
        for s in segments:
            print(*s)

if __name__ == '__main__':
    main()






