using System;
using System.Collections.Generic;

namespace LibraryManagementApi.Models;

public partial class Book
{
    public int BookId { get; set; }

    public string Title { get; set; } = string.Empty;
    public string Isbn { get; set; } =string.Empty;
    public string Author { get; set; } = string.Empty;

    public short PublishedYear{get;set;}

    public int AvailableCopies{get;set;}
    


    public DateTime Createdat { get; set; }


}
