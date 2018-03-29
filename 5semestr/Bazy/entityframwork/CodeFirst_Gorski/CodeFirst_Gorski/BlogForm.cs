using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.Entity;

namespace CodeFirst_Gorski
{
    public partial class BlogForm : Form
    {
        BlogContext bContext;
        public BlogForm()
        {
            InitializeComponent();
        }

        private void BlogForm_Load(object sender, EventArgs e)
        {

            bContext = new BlogContext();
            bContext.Blogs.Load();
            bContext.Posts.Load();
            this.blogBindingSource.DataSource = bContext.Blogs.Local.ToBindingList();
            this.postBindingSource.DataSource = bContext.Posts.Local.ToBindingList();

        }
      


        private void blogBindingNavigatorSaveItem_Click_1(object sender, EventArgs e)
        {
            bContext.SaveChanges();
        }

        private void blogDataGridView_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex > 0)
            {
                DataGridViewRow row = blogDataGridView.Rows[e.RowIndex];
               string name = row.Cells[1].Value.ToString();

                var query = bContext.Blogs.Include("Posts").Where(b => b.Name.Equals(name)).Select(b => b.Posts);
                
                foreach (var item in query) {
                    this.postBindingSource.DataSource = item.ToList();
                }

            }
            else
            {
                this.postBindingSource.DataSource = bContext.Posts.Local.ToBindingList();
            }
            
        }


    }
}
