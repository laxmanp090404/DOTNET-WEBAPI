using LibraryManagementApi.Models;
using LibraryManagementApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryManagementApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class MemberController : ControllerBase
{
    private readonly IMemberService _memberservice;
    public MemberController(IMemberService memberService)
    {
        _memberservice = memberService;
    }
   // add member 
   [HttpPost]
   public ActionResult<Member> AddMember([FromBody]Member member)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(member.FullName))
            {
                return BadRequest(new {message = "Member fullname cant be empty"});
            }
            if (string.IsNullOrWhiteSpace(member.Email))
            {
                return BadRequest(new {message = "Member Email cant be empty"});
            }
            if (string.IsNullOrWhiteSpace(member.Phone))
            {
                return BadRequest(new {message = "Phone number cant be empty"});
            }
            return Created(nameof(member),_memberservice.AddMember(member));
            
        }
        catch (System.Exception ex)
        {
            
            return StatusCode(500,new {message = "Can't create member "+ex.Message});
        }
    }
   //get all member
   [HttpGet]
   public ActionResult<IEnumerable<Member>> GetAllMembers()
    {
       try
       {
         IEnumerable<Member> ?members = _memberservice.GetAllMembers();

        if(members==null || members.Count() == 0)
        {
            return NotFound(new {message = "No members in the platform yet"});
        }
        return Ok(members);
       }
       catch (System.Exception ex)
       {
        return StatusCode(500,new {message = "Can't fetch all members "+ex.Message});

       }
    }
   // get member by id

   [HttpGet("{id}")]
   public ActionResult<Member> GetMemberBuId([FromRoute]int id)
    {
        try
        {
            Member ?member = _memberservice.GetMemberById(id);
            if(member == null)
            {
                return NotFound(new {message = $"Member with member id {id} doesnt exist in paltform"});
            }
            return Ok(member);
        }
        catch (System.Exception ex)
        {
           return StatusCode(500,new {message = "Can't fetch member with id "+id+" "+ex.Message});
    
        }
    }
    
}
