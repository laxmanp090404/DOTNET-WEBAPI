using System;
using System.Collections.Generic;

namespace LibraryManagementApi.Models;

public partial class Member
{
    public int MemberId { get; set; }

    public string FullName { get; set; } = null!;

    public string Email { get; set; } = null!;

    public string Phone { get; set; } = null!;

    public string? Address { get; set; }

    public DateTime JoinedOn { get; set; }

   


}
