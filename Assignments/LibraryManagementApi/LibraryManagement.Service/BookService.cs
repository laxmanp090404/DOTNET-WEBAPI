using LibraryManagementApi.Repository;
using LibraryManagementApi.DbContexts;
using LibraryManagementApi.Models;

namespace LibraryManagementApi.Services;

public class BookService : IBookService
{
    private readonly IRepository<int,Book> _bookRepository;
   

    private readonly LibraryContext _context;

    public BookService(IRepository<int,Book> bookRepository, LibraryContext context)
    {
        _bookRepository = bookRepository;
        _context = context;
    }

    public Book? AddBook(Book book)
    {
        book.Createdat = DateTime.UtcNow;
        return _bookRepository.Add(book);
    }

    public ICollection<Book>? GetAllBooks()
    {
        return _bookRepository.GetAll();
    }

    public Book? GetBookById(int bookId)
    {
        return _bookRepository.GetById(bookId);
    }

       // search books by title
     public ICollection<Book> SearchBooksByTitle(string searchText)
    {
        // retreives books 
        return _context.Books
            .Where(b =>
                b.Title.ToLower().Contains(searchText.ToLower())).ToList();
    }
}