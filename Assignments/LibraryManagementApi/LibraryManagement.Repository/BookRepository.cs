using LibraryManagementApi.DbContexts;
using LibraryManagementApi.Models;
using Microsoft.EntityFrameworkCore;
namespace LibraryManagementApi.Repository;

public class BookRepository : AbstractRepository<int, Book>
{
    public BookRepository(LibraryContext context) : base(context)
    {
    }

    // Get books by theri id
    public override Book? GetById(int key)
    {
        // also eager loading of category and editions
        return _context.Books.SingleOrDefault(b=>b.BookId ==key);
    }

   

   
}