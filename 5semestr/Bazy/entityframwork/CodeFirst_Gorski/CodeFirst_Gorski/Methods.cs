using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeFirst_Gorski
{
   public sealed class Methods
    {
        BlogContext bcontext;
        private static readonly Methods instance = new Methods();

        private Methods() { bcontext = new BlogContext(); }

        public static Methods Instance
        {
            get
            {
                return instance;
            }
        }
        public void addBlog(string Name, string url = null)
        {
            Blog blog = (from b in bcontext.Blogs where b.Name == Name select b).ToList().FirstOrDefault();
            if (blog != null)
            {
                if (blog.Url != url & url != null)
                {
                    Blog b = new Blog { Name = Name, Url = url };
                    bcontext.Blogs.Add(b);
                }
            }
            else
            {
                bcontext.Blogs.Add(new Blog { Name = Name, Url = url });
            }
            bcontext.SaveChanges();

        }
        public void addPost(string title, string content, string blogname, int BlogID=0)
        {
            Blog query;
            if (BlogID == 0)
            {
                query = bcontext.Blogs.Where(b => b.Name == blogname).SingleOrDefault();
            }
            else
            {
                query = bcontext.Blogs.Where(b => (b.Name == blogname) & (b.BlogID==BlogID)).SingleOrDefault();
            }
            if (query == null)
            {
                Blog blog = new Blog { Name = blogname };
                blog.Posts = new List<Post> { new Post { Title = title, Content = content } };
                bcontext.Blogs.Add(blog);
            }
            else
            {
                if (query.Posts != null)
                {
                    query.Posts.Add(new Post { Title = title, Content = content });

                }
                else
                {
                    query.Posts = new List<Post> { new Post { Title = title, Content = content } };
                }
                

            }
            bcontext.SaveChanges();
        }
        public void addUser(string username , string Description=null, string Name=null, string surname=null, string addres=null)
        {


            User u = new User { UserName = username, Description = Description, Name = Name, Addres = addres, Surname = surname };
            try
            {
                bcontext.Users.Add(u);
                bcontext.SaveChanges();
            }catch(System.Data.Entity.Infrastructure.DbUpdateException e)
            {
                Console.WriteLine("UserName {0} is taken.", username);
            } 


            
        }
        public void showUserwithName(string name)
        {
            var query = from u in bcontext.Users where u.Name == name select u.UserName;
            Console.WriteLine("UserName with name {0}: ", name);
            foreach (var item in query)
            {
                Console.WriteLine("{0} ",  item);
            }
            
        }
        public void showMostPopularBlogsSorted()
        {
            var query = bcontext.Blogs.Include("Posts").
                Select(b => new
                {
                    Blogid = b.BlogID,
                    Blogname = b.Name,
                    PostN = b.Posts.Count()


                }).OrderByDescending(b => b.PostN).ThenBy(b=>b.Blogname);
            Console.WriteLine("Blog by Updates");
            foreach (var item in query)
            {
                Console.WriteLine("BlogID: {0}, Blog Name {1}, Post Count {2}.", item.Blogid.ToString(), item.Blogname, item.PostN);

            }
        }
        public void showBlogPostCount()
        {
            var query3 = bcontext.Blogs.Select(blog => new
            {
                Blogid = blog.BlogID,
                BlogName = blog.Name,
                counting = blog.Posts.Count()

            });
            foreach (var item in query3)
            {
                Console.WriteLine("BlogID: {0}, Blog Name {1}, Post Count {2}.", item.Blogid.ToString(), item.BlogName, item.counting);

            }
        }
        public void showBlogPost()
        {
            var query = from b in bcontext.Blogs
                        join p in bcontext.Posts
                        on b.BlogID equals p.BlogID
                        select new
                        {
                            Blogid = b.BlogID,
                            BlogName = b.Name,
                            title = p.Title
                        };

            foreach (var item in query)
            {
                Console.WriteLine("BlogID: {0}, Blog Name {1}, Post Title {2}.", item.Blogid.ToString(), item.BlogName, item.title);

            }
            Console.WriteLine("\n");
            var query1 = bcontext.Blogs.Join(bcontext.Posts, blog => blog.BlogID, post => post.BlogID,
                (blog, post) => new
                {
                    Blogid = blog.BlogID,
                    BlogName = blog.Name,
                    title = post.Title
                }).ToList();
            foreach (var item in query)
            {
                Console.WriteLine("BlogID: {0}, Blog Name {1}, Post Title {2}.", item.Blogid.ToString(), item.BlogName, item.title);

            }
            Console.WriteLine("\n");
            IQueryable<Blog> query2 = bcontext.Blogs.Include("Posts");
            foreach (Blog item in query2)
            {
                Console.WriteLine("BlogID: {0}, Blog Name {1}", item.BlogID.ToString(), item.Name);
                foreach (Post p in item.Posts)
                {
                    Console.WriteLine("Post Title: {0}. ", p.Title);
                }

            }
        }
    }
}
