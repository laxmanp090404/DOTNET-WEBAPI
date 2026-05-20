using LibraryManagementApi.DbContexts;
using Microsoft.EntityFrameworkCore;
using System;

using System.Collections.Generic;
using System.Linq;

namespace LibraryManagementApi.Repository;

public abstract class AbstractRepository<K, T> : IRepository<K, T> where T : class where K : notnull
{
    // faster access
    protected LibraryContext _context;

    public AbstractRepository(LibraryContext context)
    {
        _context = context;
    }

    // virtual methods to allow overriding if required
    public virtual T Add(T entity)
    {
        try
        {
            _context.Set<T>().Add(entity);
            _context.SaveChanges();
            return entity;
        }
        catch (Exception ex)
        {
            throw new Exception($"Error adding entity of type {typeof(T).Name}", ex);
        }
    }

    public virtual T Delete(K key)
    {
        try
        {
            var entity = GetById(key);
            if (entity == null)
            {
                throw new Exception($"Entity of type {typeof(T).Name} with key {key} not found for deletion.");
            }

            _context.Set<T>().Remove(entity);
            _context.SaveChanges();
            return entity;
        }
        // catch (EntityNotFoundException)
        // {
        //     throw; 
        // }
        catch (Exception ex)
        {
            throw new Exception($"Error deleting entity of type {typeof(T).Name}", ex);
        }
    }

    public virtual ICollection<T> GetAll()
    {
        try
        {
            return _context.Set<T>().ToList();
        }
        catch (Exception ex)
        {
            throw new Exception($"Error retrieving all entities of type {typeof(T).Name}", ex);
        }
    }

    // id ambiguous
    public abstract T? GetById(K key);

    public virtual T Update(T entity)
    {
        try
        {
            _context.Set<T>().Update(entity);
            _context.SaveChanges();
            return entity;
        }
        catch (Exception ex)
        {
            throw new Exception($"Error updating entity of type {typeof(T).Name}", ex);
        }
    }
}