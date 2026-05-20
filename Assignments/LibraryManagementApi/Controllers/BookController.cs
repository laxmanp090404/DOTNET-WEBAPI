using LibraryManagementApi.Models;
using LibraryManagementApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryManagementApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BookController : ControllerBase
{
    private readonly IBookService _bookservice;
    public BookController(IBookService bookservice)
    {
     _bookservice = bookservice;   
    }
    //add book
    [HttpPost]
    public ActionResult<Book> AddBook([FromBody]Book book)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(book.Title))
            {
                return BadRequest(new {message = "Book title cant be empty"});
            }
            if (string.IsNullOrWhiteSpace(book.Author))
            {
                return BadRequest(new {message = "Author cant be empty"});
            }
            if(book.AvailableCopies < 0)
            {
                return BadRequest(new {message = "Available copies has to 0 or more"});
            }
            return Created(nameof(book),_bookservice.AddBook(book));
            
        }
        catch (System.Exception e)
        {
            
           return StatusCode(500,new {message = e.Message});
        }
    }

    //get all books
    [HttpGet]
    public ActionResult<IEnumerable<Book>> GetAllBook()
    {
        try
        {
            IEnumerable<Book>? books = _bookservice.GetAllBooks();
            if(books == null || books.Count() == 0)
            {
                return NotFound(new {message="No books currently in the system"});
            }
            return Ok(books);
        
        }
        catch (System.Exception e)
        {
            return StatusCode(500,new {message = e.Message});            
        }
    }
    // get book by id
    [HttpGet("{id}")]
    public ActionResult<Book> GetOneBook(int id)
    {
        try
        {
            Book ?book = _bookservice.GetBookById(id);
            if(book == null)
            {
                return NotFound(new {message = "Book Not found with given Id"});
            }
            return Ok(book);
        }
        catch (System.Exception e)
        {
         return StatusCode(500,new {message = e.Message}); 
        }
    }

    //last
    // GET /api/books/search?title=clean
    [HttpGet("search")]
    public ActionResult<IEnumerable<Book>> SearchBooks(string title)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(title))
            {
                return BadRequest(new {message="Can't search for empty title"});
            }
            IEnumerable<Book>? resbooks = _bookservice.SearchBooksByTitle(title);
            if(resbooks == null || resbooks.Count() == 0)
            {
                return NotFound(new {message = "No books match the given title "+title});
            }
            return Ok(resbooks);
        }
        catch (System.Exception e)
        {
            return StatusCode(500,new {message = e.Message});
            
        }
    }
}
