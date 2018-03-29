using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeFirst_Gorski
{
    class BlogContext:DbContext
    {
        public DbSet<Blog> Blogs { get; set; }
        public DbSet<Post> Posts { get; set; }
        public DbSet<User> Users { get; set; }
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>()
            .Property(u => u.Description)
            .HasColumnName("DetailedDescription");

            modelBuilder.Entity<User>()
    .Map(m =>
    {
        m.Properties(t => new { t.UserName, t.Description });
        m.ToTable("User");
    })
    .Map(m =>
    {
        m.Properties(t => new { t.Name, t.Surname, t.Addres });
        m.ToTable("UserData");
    });
        }

    }
}
