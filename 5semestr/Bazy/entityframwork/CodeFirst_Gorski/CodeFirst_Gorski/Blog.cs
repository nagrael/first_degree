using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeFirst_Gorski
{
    class Blog
    {
        public int BlogID { get; set; }
        public string Name { get; set; }
        public string Url { get; set; }
        public List<Post> Posts { get; set; }
    }
}
