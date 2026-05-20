using LibraryManagementApi.Models;

namespace LibraryManagementApi.Services;

public interface IBookService
{
    //add a book
    Book? AddBook(Book book);
    // get all books (irrespective of status)
    ICollection<Book>? GetAllBooks();
  
    // search book by title
    ICollection<Book>? SearchBooksByTitle(string title);
    
    //get books by Id
    Book? GetBookById(int bookId);

    
}