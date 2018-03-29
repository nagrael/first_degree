namespace CodeFirst_Gorski.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class UpdateUser : DbMigration
    {
        public override void Up()
        {
            RenameTable(name: "dbo.Users", newName: "User");
            CreateTable(
                "dbo.UserData",
                c => new
                    {
                        UserName = c.String(nullable: false, maxLength: 128),
                        Name = c.String(),
                        Surname = c.String(),
                        Addres = c.String(),
                    })
                .PrimaryKey(t => t.UserName)
                .ForeignKey("dbo.User", t => t.UserName)
                .Index(t => t.UserName);
            
            DropColumn("dbo.User", "Name");
            DropColumn("dbo.User", "Surname");
            DropColumn("dbo.User", "Addres");
        }
        
        public override void Down()
        {
            AddColumn("dbo.User", "Addres", c => c.String());
            AddColumn("dbo.User", "Surname", c => c.String());
            AddColumn("dbo.User", "Name", c => c.String());
            DropForeignKey("dbo.UserData", "UserName", "dbo.User");
            DropIndex("dbo.UserData", new[] { "UserName" });
            DropTable("dbo.UserData");
            RenameTable(name: "dbo.User", newName: "Users");
        }
    }
}
