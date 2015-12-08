using System;
using System.Collections.Generic;
using System.Text;

namespace MemoryImage2
{
    class B
    {
        public int i = 0;
        public int j = 5;
        public static int si = 3;
        public static int sj = 0;
    }
    class A {
        public int g1 = 4;
        public int g2 = 0;

        public void trace(int p1, int p2) {
            B bp = new B();
            if ((p1/3)*3 == p1) 
            {
	            bp.i = bp.j + 1;
	            B.si++;
	            B.sj = B.sj + p1 + p2;
                this.trace(p1-1, p2-1);  //L1:
	            g1++;
	            g2 = g2 - p1 - p2;
            }else {
                if (((p1/3)*3+2) == p1) {
	                 bp.i = bp.j + 1;
	                 g1++;
	                 g2 = g2 + p1 + p2;
	                 this.trace(p1-1, p2+1); //L2:
	                 B.si++;
	                 B.sj = B.sj - p1 - p2;
                } else {
	                 bp.i = bp.j + 1;
	                 Console.WriteLine(p1 + "   " + p2 + "   " + bp.i + 
                         "   " + bp.j + "  " + B.si + "   " + B.sj + "  " + 
                         g1 + "   " + g2);
	           }
           }
       }
    }


    class MemoryImage2
    {
        static void Main(string[] args)
        {
            A ap = new A();
            ap.trace(6, 4); // L3:
            Console.WriteLine(ap.g1 + "   " + ap.g2);;
        }
    }
}
