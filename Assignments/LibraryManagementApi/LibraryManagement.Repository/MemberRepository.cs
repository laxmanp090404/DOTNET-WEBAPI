using LibraryManagementApi.DbContexts;
using LibraryManagementApi.Models;

namespace LibraryManagementApi.Repository;

public class MemberRepository : AbstractRepository<int, Member>
{
    public MemberRepository(LibraryContext context) : base(context)
    {
    }

    public override Member? GetById(int key)
    {
        //LINQ based
        return _context.Members.SingleOrDefault(m => m.MemberId == key);
    }
    public override ICollection<Member> GetAll()
    {
        return _context.Members.ToList();
    }

   
}