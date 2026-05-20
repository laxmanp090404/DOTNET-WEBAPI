using System;
using System.Collections.Generic;
using LibraryManagementApi.Models;

using Microsoft.EntityFrameworkCore;

namespace LibraryManagementApi.DbContexts;

public partial class LibraryContext : DbContext
{
    public LibraryContext()
    {
    }

    public LibraryContext(DbContextOptions<LibraryContext> options) : base(options)
    {
    }

    public virtual DbSet<Book> Books { get; set; }


    public virtual DbSet<Member> Members { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Member>(entity =>
        {
            entity.HasKey(e => e.MemberId);

            entity.HasIndex(e => e.Email).IsUnique();

            entity.HasIndex(e => e.Phone).IsUnique();

            entity.Property(e => e.JoinedOn)
       .HasColumnType("timestamp with time zone");


        });

        modelBuilder.Entity<Book>(entity =>
        {
            entity.HasKey(e => e.BookId);

            entity.HasIndex(e => e.Isbn)
                  .IsUnique();

            entity.Property(e => e.Createdat)
                  .HasColumnType("timestamp with time zone")
                  .HasDefaultValueSql("now()");

        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
