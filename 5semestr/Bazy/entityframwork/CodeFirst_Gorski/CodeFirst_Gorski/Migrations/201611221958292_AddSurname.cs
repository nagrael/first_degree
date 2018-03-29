namespace CodeFirst_Gorski.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class AddSurname : DbMigration
    {
        public override void Up()
        {
            AddColumn("dbo.Users", "Name", c => c.String());
            AddColumn("dbo.Users", "Surname", c => c.String());
            AddColumn("dbo.Users", "Addres", c => c.String());
        }
        
        public override void Down()
        {
            DropColumn("dbo.Users", "Addres");
            DropColumn("dbo.Users", "Surname");
            DropColumn("dbo.Users", "Name");
        }
    }
}
