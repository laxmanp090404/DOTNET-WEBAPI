# Azure Cloud Project – End-to-End ASP.NET Core Web API on Microsoft Azure

## Overview

This project demonstrates how to build, secure, and deploy a production-style **ASP.NET Core 10 Web API** using Microsoft Azure services and modern cloud best practices.

The application is deployed to Azure App Service, securely accesses secrets from Azure Key Vault using Managed Identity, and stores files in Azure Blob Storage without embedding credentials in the source code.

---

# Architecture

```
                 +----------------------+
                 |    Client / Browser  |
                 +----------+-----------+
                            |
                            |
                    HTTPS Requests
                            |
                            ▼
                Azure App Service (Web API)
                            |
        -----------------------------------------
        |                                       |
        | Managed Identity                      |
        ▼                                       ▼
 Azure Key Vault                      Azure Blob Storage
 (Secrets & Keys)                    (Upload / Download)
```

---

# Azure Services Used

## 1. Azure CLI

Azure CLI was used to provision and manage all Azure resources from the command line.

Common tasks included:

* Logging into Azure
* Creating resource groups
* Creating storage accounts
* Creating Key Vaults
* Deploying App Services
* Managing Managed Identity
* Configuring application settings

**Benefits**

* Infrastructure automation
* Repeatable deployments
* Scriptable resource management

---

## 2. Resource Group

A Resource Group acts as a logical container for Azure resources.

Resources included:

* App Service
* App Service Plan
* Storage Account
* Blob Container
* Key Vault
* Managed Identity

**Benefits**

* Centralized management
* Easier cleanup
* Access control
* Cost tracking

---

## 3. Azure Key Vault

Azure Key Vault securely stores sensitive information such as:

* Storage connection strings (if needed)
* API secrets
* Certificates
* Encryption keys

Instead of storing secrets in:

* appsettings.json
* source code
* Git repositories

the application retrieves them securely at runtime.

**Benefits**

* Secure secret management
* Centralized credential storage
* Automatic secret rotation support
* Improved compliance

---

## 4. Azure Blob Storage

Azure Blob Storage provides scalable object storage for files.

Example operations:

* Upload files
* Download files
* Store images
* Store documents
* Store backups

The Web API communicates with Blob Storage using the Azure Storage SDK.

**Benefits**

* Highly scalable
* Durable
* Cost-effective
* Secure

---

## 5. ASP.NET Core 10 Web API

The backend application exposes REST endpoints that interact with Azure services.

Typical responsibilities:

* Accept client requests
* Upload files
* Download files
* Read configuration
* Authenticate securely
* Access Azure resources

---

## 6. Azure App Service

Azure App Service hosts the ASP.NET Core Web API.

Deployment features include:

* Continuous deployment
* HTTPS support
* Auto-scaling
* Managed runtime
* Monitoring
* High availability

The application runs without managing virtual machines or servers.

---

## 7. Managed Identity

Managed Identity provides the application with an automatically managed Azure identity.

Instead of storing credentials:

```
Storage Key
Client Secret
Password
Certificate
```

Azure automatically authenticates the application.

The App Service identity is granted permission to access Azure resources.

**Benefits**

* No hardcoded credentials
* No secret expiration
* Simplified authentication
* Improved security

---

## 8. Key Vault Integration

The application uses Managed Identity to securely access Azure Key Vault.

Authentication flow:

```
App Service
      │
      │ Managed Identity
      ▼
Azure Active Directory
      │
      ▼
Azure Key Vault
      │
      ▼
Returns Secret
```

No passwords or client secrets are required.

---

## 9. Blob Upload & Download

The Web API supports file operations with Azure Blob Storage.

Typical workflow:

```
Client
   │
   │ Upload File
   ▼
ASP.NET Core API
   │
   ▼
Azure Blob Storage
```

For downloads:

```
Blob Storage
      │
      ▼
ASP.NET Core API
      │
      ▼
Client
```

This enables cloud-based file storage while keeping the application lightweight.

---

## 10. Cloud Deployment

The application was deployed to Azure App Service.

Deployment steps included:

* Publishing the application
* Configuring environment settings
* Connecting Azure resources
* Verifying cloud execution
* Testing endpoints

This mirrors a real-world deployment pipeline for cloud-hosted applications.

---

## 11. Passwordless Authentication

A key security feature of this project is passwordless authentication.

Instead of storing:

* Access keys
* Client secrets
* Passwords
* Connection strings

the application uses:

```
Managed Identity
        +
Azure Active Directory
        +
Role-Based Access Control (RBAC)
```

This approach significantly reduces the risk of credential leakage and follows Microsoft's recommended security practices.

---

# Security Best Practices Demonstrated

* No hardcoded credentials
* Managed Identity authentication
* Secure secret storage with Key Vault
* Role-Based Access Control (RBAC)
* HTTPS deployment
* Least-privilege access
* Cloud-native authentication

---

# Project Workflow

```
Azure CLI
      │
      ▼
Create Resource Group
      │
      ▼
Create Storage Account
      │
      ▼
Create Blob Container
      │
      ▼
Create Key Vault
      │
      ▼
Store Secrets
      │
      ▼
Create App Service
      │
      ▼
Enable Managed Identity
      │
      ▼
Grant Key Vault Permissions
      │
      ▼
Deploy ASP.NET Core API
      │
      ▼
Application Retrieves Secrets
      │
      ▼
Application Accesses Blob Storage
      │
      ▼
Users Upload & Download Files
```

---

# Key Azure Concepts Learned

* Azure Resource Management
* Azure CLI
* Resource Groups
* Azure App Service
* Azure Key Vault
* Azure Blob Storage
* Managed Identity
* Azure Active Directory integration
* Role-Based Access Control (RBAC)
* Secure cloud authentication
* Cloud deployment strategies
* Passwordless application development

---

# Learning Outcomes

By completing this project, you gained practical experience in:

* Provisioning Azure resources using the Azure CLI
* Organizing resources with Resource Groups
* Hosting APIs on Azure App Service
* Storing and retrieving secrets securely with Azure Key Vault
* Managing file storage using Azure Blob Storage
* Implementing Managed Identity for secure authentication
* Integrating Azure services into an ASP.NET Core Web API
* Deploying cloud-native applications
* Applying passwordless authentication and security best practices

---

# Conclusion

This project demonstrates a production-style Azure application architecture that combines secure authentication, cloud storage, secret management, and scalable web hosting. By leveraging Azure App Service, Managed Identity, Key Vault, and Blob Storage, the application follows modern cloud-native principles, eliminating hardcoded credentials while enabling secure, scalable, and maintainable deployments.
