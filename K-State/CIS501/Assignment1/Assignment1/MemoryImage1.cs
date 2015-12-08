using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ExecutionEnvironment
{
    class A
    {
        public int a = 5;
        public static int sa = 9;
        public void Trace_MeA(B bp, int i)
        {
            a = a + bp.b;
            sa++;
            if (i < sa)
            {
                bp.Trace_MeB(a);
    // L1: return address
            }
            else if (sa > a)
            {
                B.sb++;
                Trace_MeA(new B(), B.sb);
    // L2: return address
                B.sb -= 4;
            }
        }
    }

    class B
    {
        A ap = new A();
        public int b = 12;
        public static int sb = 3;
        public void Trace_MeB(int j)
        {
            sb++;
            A.sa--;
            ap.a = b + j;
            if (j < A.sa * 2 + sb)
            {
                Trace_MeB(sb*j);
     // L3: return address
                sb -= 2;
            }
            else if (ap.a+A.sa > b + j)
            {
                ap.Trace_MeA(this, j + 3);
    // L4: return address
            }
        }
        }

    class Program
    {
        static void Main(string[] args)
        {
            A ap = new A();
            B bp = new B();
            ap.Trace_MeA(bp, 3);  
   // L5: return address
            Console.WriteLine("A.sa = " + A.sa + ",  B.sb = " + B.sb);
        }
    }
}
