using LibraryManagementApi.Models;

namespace LibraryManagementApi.Services;

public interface IMemberService
{
    // add a member
    Member? AddMember(Member member);
    // get all members
    ICollection<Member>? GetAllMembers();
    // get member by his id
    Member? GetMemberById(int memberId);

   
   
}