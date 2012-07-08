using System;

namespace openpass_cs
{
	class MainClass
	{
		public static long algo(long password, string operazioni)
		{
		    int num = 0;
		    bool flag = true;
		    long num1 = (long)0;
		    long num2 = (long)0;
		    num = 0;
		    while (true)
		    {
		        bool length = num < operazioni.Length;
		        if (!length)
		        {
		            break;
		        }
		        char chr = operazioni[num];
		        num1 = num1 & -1;
		        num2 = num2 & -1;
		        char chr1 = chr;
		        switch (chr1)
		        {
		            case '1':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 & -128;
		                num1 = num1 >> 7;
		                num2 = num2 << 25;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '2':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 & -16;
		                num1 = num1 >> 4;
		                num2 = num2 << 28;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '3':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 & (long)-8;
		                num1 = num1 >> 3;
		                num2 = num2 << 29;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '4':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 << 1;
		                num2 = num2 >> 31;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '5':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 << 5;
		                num2 = num2 >> 27;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '6':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 << 12;
		                num2 = num2 >> 20;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '7':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 & (long)65280;
		                num1 = num1 + ((num2 & (long)255) << 24);
		                num1 = num1 + ((num2 & (long)16711680) >> 16);
		                num2 = (num2 & (long)-16777216) >> 8;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '8':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = num2 & (long)65535;
		                num1 = num1 << 16;
		                num1 = num1 + (num2 >> 24);
		                num2 = num2 & (long)16711680;
		                num2 = num2 >> 8;
		                num1 = num1 + num2;
		                flag = false;
		                break;
		            }
		            case '9':
		            {
		                length = !flag;
		                if (!length)
		                {
		                    num2 = password;
		                }
		                num1 = ~num2;
		                flag = false;
		                break;
		            }
		            default:
		            {
		                num1 = num2;
		                break;
		            }
		        }
		        num2 = num1;
		        num++;
		    }
		    long num3 = num1 & -1;
		    return num3;
		}
			

		public static void Main (string[] args)
		{
			Console.WriteLine (algo (12345,"603356072"));
		}
	}
}
