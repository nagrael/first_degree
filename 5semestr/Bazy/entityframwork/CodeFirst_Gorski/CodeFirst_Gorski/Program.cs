using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeFirst_Gorski
{
    class Program
    {
       
        static void Main(string[] args)
        {
            //Console.WriteLine("Podaj Username: ");
            //string usename = Console.ReadLine();
            // Console.WriteLine("Podaj imie: ");
            // string name = Console.ReadLine();
            //Console.WriteLine("Podaj znazwisko: ");
            //string surname = Console.ReadLine();
            //Methods.Instance.addUser(username:"tyuop", Name:"Kan", surname:"Han");
           // Methods.Instance.showBlogPost();
            BlogForm a = new BlogForm();
            a.ShowDialog();
            Console.ReadKey();
        }

    }
}
