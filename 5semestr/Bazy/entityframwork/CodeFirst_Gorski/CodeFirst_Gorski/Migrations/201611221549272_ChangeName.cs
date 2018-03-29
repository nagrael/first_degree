namespace CodeFirst_Gorski.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class ChangeName : DbMigration
    {
        public override void Up()
        {
            RenameColumn(table: "dbo.Users", name: "Description", newName: "DetailedDescription");
        }
        
        public override void Down()
        {
            RenameColumn(table: "dbo.Users", name: "DetailedDescription", newName: "Description");
        }
    }
}
