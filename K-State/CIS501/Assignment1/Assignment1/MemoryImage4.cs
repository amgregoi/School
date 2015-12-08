using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MemryImage4
{
    class A
    {
        public int a = 3;
        public static int sa = 4;

        public virtual C f(int i, int j)
        {
            A ap = new C();
            B bp = new B();
            C cp;
            i -= 2;
            j -= 3;
            sa--;
            if (i > 0)
            {
                cp = ap.f(i, j);  // L1 
                cp.a++;
                cp.c--;              
            }
            else if (j > 0)
            {
                bp = bp.g(i+j);  // L2 
                cp = new C();
                cp.a = bp.a + sa;
                cp.b = bp.b - sa;
            }
            else cp = new C();
            return cp;
        }

        public virtual B g(int k)
        {
            A ap;
            B bp = new B();
            sa--;
            if (sa > 0)
            {
                ap = new A();
                bp = ap.g(sa); //  L3  
                bp.b += 3;
                bp.a--;
            }
            else if (sa > a)
            {
                ap = new C();
                bp = ap.f(a, sa);  // L4
                bp.b -= 4;
                bp.a -= 3;
            }
            return bp;    
        }
    }

    class B : A
    {
        public int b = 8;

        public override C f(int i, int j)
        {
            B bp = new B();
            C cp = new C();

            sa--;
            if (sa > bp.b - 7)
            {
                cp = bp.f(sa, bp.a);  // L5
                cp.c = bp.a;
                cp.b -= 2;
                cp.a -= 4;
            }
            else if (sa > bp.a - 6)
            {
                bp = cp.g(sa);  // L6 
                cp.c += sa;
                cp.b -= bp.b;
            }
            return cp;
        }
    }

    class C: B
    {
        public int c = 5;

        public override B g(int k)
        {
            C cp = new C();
            c += 2;
            b += sa;
            a = a - sa;
            if (sa > a)
            {
                cp = this.f(sa, c);  // L7
                sa++;
                cp.a += 2;
                cp.b += cp.c;          
            }
            return cp;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            A ap = new A();
            C cp = ap.f(4, -2); // L8
            Console.WriteLine("cp.a = " + cp.a +"\tcp.b = " + cp.b + "\tcp.c = " + cp.c + "\nC.sa = " + C.sa);
        }
    }
}
