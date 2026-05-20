using System;
using System.Collections.Generic;
using System.Linq;
using LibraryManagementApi.Repository;
using LibraryManagementApi.Models;

namespace LibraryManagementApi.Services;

public class MemberService : IMemberService
{
    // private readonly faster access
    private readonly IRepository<int,Member> _memberRepository;

    // dependency injection
    public MemberService(IRepository<int,Member> memberRepository)
    {
        _memberRepository = memberRepository;
    }

    public Member? AddMember(Member member)
    {
        try
        {
            member.JoinedOn = DateTime.UtcNow;
            return _memberRepository.Add(member);
        }
        catch (Exception ex)
        {
            throw new Exception($"Failed to add member : {ex.InnerException?.Message ?? ex.Message}");
        }
    }

 
    public ICollection<Member>? GetAllMembers()
    {
        try
        {
            var members = _memberRepository.GetAll();
            return members;
        }
   
        catch (Exception ex) { throw new Exception("Failed to fetch members", ex); }
    }

    public Member? GetMemberById(int memberId)
    {
        try
        {
            var member = _memberRepository.GetById(memberId);
            return member;
        }
        catch (Exception ex) { throw new Exception("Failed to fetch member", ex); }
    }

    
}