using System;
using System.Collections.Generic;
using System.Text;

namespace MemoryImage3
{
    class A
    {
        public int a = 5;

        internal virtual void f(A ap)
        {
            a++;
            if (ap.a < 3) this.f(ap); //L1:
            else if (a < 0) ap.g(this);  //L2:
            a -= 4;
        }
        internal virtual void g(A ap)
        {
            B.sb++;
            if (a < 3) this.f(ap);  //L3:
            else if (ap.a > 0) ap.g(this); //L4:
            a += B.sb;
        }
    }
    class B : A
    {
        public int b = 10;
        public static int sb = 0;

        internal override void f(A ap)
        {
            C cp = (C)ap;
            int i = ap.a * 2;
            a -= 2;
            cp.c -= 3;
            B.sb++;
            if (a > 2) this.g(ap);  // L5:
            else if (a > 0) this.f(ap);  //L6: 
            a = a + cp.a - i;
        }
        internal override void g(A ap)
        {
            C cp = (C)ap;
            int j = sb;
            sb += 2;
            a -= 1;
            cp.c++;
            if (ap.a > 0) cp.f(this); //L7:
            else if (a > 0) this.g(ap);  //L8:
            b = b + j * 2;
            sb -= 3;
            a = a + sb;
        }
    }
    class C : A
    {
        public int c = 14;

        internal override void f(A ap)
        {
            B bp = (B)ap;
            int k = B.sb * bp.b;
            a -= 3;
            c -= 2;
            bp.a -= 1;
            if (ap.a > k) ap.f(this); //L9:
            else if (c > a) this.g(ap); //L10:
            a += 1;
            c += a;
            bp.b += 3;
        }
        internal override void g(A ap)
        {
            B bp = (B)ap;
            bp.a = bp.a - B.sb;
            if (bp.a > 2) this.g(ap);  //L11:
            else if (a > 0) this.f(ap);  //L12:
            a++;
            bp.b--;         
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            B bp = new B();
            C cp = new C();
            bp.g(cp);  //L13:
            Console.WriteLine("bp.a = " + bp.a + ",  bp.b = "
                    + bp.b);
            Console.WriteLine("cp.a = " + cp.a + ",  cp.c = "
                    + cp.c);
            Console.WriteLine("B.sb = " + B.sb);
        }
    }
}
