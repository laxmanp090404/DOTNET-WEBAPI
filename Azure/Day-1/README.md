# Azure  — VMs, SQL Database, Storage Blob, Static Website Hosting

---

## 1. Azure Virtual Machines (VMs)

### Core Concepts
- **VM** = IaaS compute resource; you manage OS, runtime, and applications. Azure manages the underlying hardware, virtualization, and networking fabric.
- **Image**: Template used to create a VM (Marketplace images, custom images, Azure Compute Gallery / Shared Image Gallery).
- **VM Size/SKU**: Defines vCPU, RAM, temp storage, max data disks, and network bandwidth. Families: B (burstable), D (general purpose), E (memory optimized), F (compute optimized), N (GPU), L (storage optimized).
- **Disks**:
  - OS Disk (mandatory, default 127 GB cap depends on type) and Data Disks (attached separately).
  - Disk types: Standard HDD, Standard SSD, Premium SSD, Ultra Disk (performance/cost trade-off in that order).
  - Managed Disks (Azure-managed storage account behind the scenes) vs unmanaged (legacy, avoid).
  - Temporary disk (D:\ on Windows, /dev/sdb on Linux) — ephemeral, not persisted on deallocate/migration.
- **Networking**:
  - NIC (Network Interface Card) attached to a VM, placed inside a Subnet within a Virtual Network (VNet).
  - Public IP (optional) for internet access; Private IP for internal communication.
  - NSG (Network Security Group): stateful firewall rules (Allow/Deny) at subnet or NIC level, evaluated by priority (lower number = higher priority).
- **Availability**:
  - Availability Set: groups VMs into Fault Domains (separate power/network) and Update Domains (separate maintenance reboot groups) — protects against single datacenter hardware/maintenance failure.
  - Availability Zone: physically separate datacenters within a region — protects against datacenter-level failure.
  - VM Scale Sets (VMSS): auto-scaling group of identical VMs based on metrics/schedule.
- **VM States**: Running, Stopped (still billed for compute), Stopped (Deallocated) (not billed for compute, but still billed for disks/IP).
- **Extensions**: Post-deployment automation agents (Custom Script Extension, VM Agent, Diagnostics Extension).
- **Identity**: Managed Identity (System-assigned or User-assigned) lets a VM authenticate to other Azure services without storing credentials.

### Typical Workflow (Exam + Hands-on)
1. Plan: choose region, resource group, VM size, OS image.
2. Create VNet + Subnet (or use existing).
3. Create NSG and define inbound/outbound rules (e.g., allow RDP 3389 / SSH 22 only from your IP).
4. Deploy VM:
   - Portal: Create a resource → Virtual Machine → fill Basics (auth: password or SSH key), Disks, Networking, Management, Advanced, Tags → Review + Create.
   - CLI: `az vm create --resource-group RG --name VM1 --image Ubuntu2204 --admin-username azureuser --generate-ssh-keys`
   - ARM/Bicep/Terraform for IaC-based deployment.
5. Connect: RDP (Windows) or SSH (Linux), or Azure Bastion for browser-based secure access without exposing public IP.
6. Configure: install software, attach data disks, run extensions/scripts.
7. Manage lifecycle: resize VM (may require stop/deallocate), start/stop/deallocate, snapshot disks for backup, enable Azure Backup.
8. Monitor: Azure Monitor, boot diagnostics, metrics (CPU, disk, network), Azure Advisor for right-sizing recommendations.
9. Scale (optional): convert to VMSS or add to a Scale Set; configure autoscale rules.
10. Decommission: deallocate → delete VM → delete disks/NIC/public IP (these aren't auto-deleted) → delete NSG/VNet if unused.

### Exam Tips
- Know billing difference: Stopped vs Stopped(Deallocated).
- Know NSG rule evaluation order and default rules (AllowVnetInBound, AllowAzureLoadBalancerInBound, DenyAllInBound).
- Resizing a VM may require it to be in a different hardware cluster — sometimes requires deallocation.
- Know when to use Availability Set vs Availability Zone vs Scale Set (99.95% vs 99.99% SLA).
- Managed Disks vs unmanaged — almost always pick Managed in current exams.

---

## 2. Azure SQL Database

### Core Concepts
- **PaaS** relational database service (no OS/patch management); built on SQL Server engine.
- **Deployment models**:
  - Single Database — isolated DB with its own resources.
  - Elastic Pool — shared resources (DTUs/vCores) across multiple databases with variable usage patterns; cost-efficient for many small DBs.
  - Managed Instance — near 100% SQL Server compatibility, supports cross-database queries, SQL Agent, linked servers; for lift-and-shift migrations.
- **Purchasing models**:
  - DTU-based (Basic, Standard, Premium) — bundled compute+storage+IO units.
  - vCore-based (General Purpose, Business Critical, Hyperscale) — separate compute/storage, more control, reserved capacity discounts.
- **Logical Server**: A management boundary (not a real VM) that hosts one or more databases; defines server-level firewall rules, admin login, and collation.
- **Security**:
  - Firewall rules (server-level and database-level) — IP allow-listing.
  - "Allow Azure services and resources to access this server" toggle.
  - Azure AD (Entra ID) authentication alongside SQL authentication.
  - Always Encrypted, Transparent Data Encryption (TDE — on by default), Dynamic Data Masking, Row-Level Security.
  - Private Link / VNet Service Endpoints for private connectivity.
- **High Availability & DR**:
  - Built-in HA (zone-redundant for Premium/Business Critical).
  - Automated backups (full/diff/log) with Point-in-Time Restore (PITR).
  - Geo-replication (active geo-replication) and Auto-failover groups for DR across regions.
  - Long-term retention (LTR) policies for compliance.
- **Performance**:
  - DTU/vCore scaling (manual or via Hyperscale auto-scale).
  - Query Performance Insight, Automatic Tuning, Index recommendations.
  - Serverless tier — auto-pause/resume, billed per second of usage.

### Typical Workflow (Exam + Hands-on)
1. Create a Logical Server (region, admin credentials, AD admin optional).
2. Configure server firewall rule(s) to allow your client IP and/or Azure services.
3. Create the SQL Database: choose purchasing model (DTU/vCore), service tier, and either Single DB or add to an Elastic Pool.
4. Connect using SSMS, Azure Data Studio, or `sqlcmd`, or the in-browser Query Editor in the portal.
5. Configure security: set up Azure AD admin, enable Defender for SQL, configure Dynamic Data Masking if needed.
6. Set up backups/retention: configure PITR window, LTR policy if required.
7. Configure scaling: adjust DTUs/vCores, or enable autoscale (Hyperscale/serverless).
8. Set up DR (if required): configure geo-replication or auto-failover group to a secondary region.
9. Monitor: Query Performance Insight, Azure Monitor metrics (DTU%, deadlocks, storage), set alerts.
10. Decommission: delete database → delete logical server (only possible once all databases are removed).

### Exam Tips
- Logical server itself has no compute cost; only databases/elastic pools are billed.
- TDE is enabled by default and cannot be disabled in many recent SKUs.
- Elastic Pool is ideal for "many databases, unpredictable/variable usage" scenarios — a classic exam scenario phrase.
- Managed Instance is the answer when the scenario says "needs SQL Agent / cross-database queries / minimal app changes during migration."
- Auto-failover groups give you a read-write listener endpoint that auto-redirects after failover — different from manual geo-replication.

---

## 3. Azure Storage — Containers / Blob Storage

### Core Concepts
- **Storage Account**: top-level namespace providing access to Blob, File, Queue, Table, and Disk storage. Globally unique name, becomes part of the endpoint URL.
- **Performance tiers**: Standard (HDD-backed, general) vs Premium (SSD-backed, low latency).
- **Redundancy options** (durability):
  - LRS (Locally Redundant) — 3 copies, single datacenter.
  - ZRS (Zone Redundant) — copies across 3 availability zones in region.
  - GRS (Geo-Redundant) — LRS + async copy to paired region.
  - GZRS — ZRS + geo-replication to paired region (highest durability for most exams).
  - RA-GRS/RA-GZRS — adds read access to the secondary region.
- **Blob types**:
  - Block Blob — most common, for files/documents/media, made of blocks.
  - Append Blob — optimized for append operations (e.g., logging).
  - Page Blob — random read/write, used for VHD/VM disks.
- **Access tiers** (cost optimization, block blobs only):
  - Hot — frequent access.
  - Cool — infrequent access (min 30-day storage), lower storage cost, higher access cost.
  - Cold — infrequent access (min 90-day), even lower storage cost.
  - Archive — rarely accessed (min 180-day), lowest cost, requires rehydration (hours) before access.
  - Lifecycle Management policies automate tier transitions/deletion based on rules (e.g., age of blob).
- **Containers**: Logical grouping of blobs (like a folder/bucket); access level set per container — Private, Blob (anonymous read for blobs only), Container (anonymous read for container+blobs).
- **Security & Access**:
  - Access Keys (account-level, full control — rotate periodically).
  - Shared Access Signature (SAS): time-limited, scoped token (Account SAS, Service SAS, User Delegation SAS — the most secure, tied to Azure AD identity).
  - Azure AD (RBAC) — roles like Storage Blob Data Reader/Contributor/Owner.
  - Storage Firewall & Virtual Networks — restrict access by IP/VNet.
  - Encryption at rest (default, Microsoft-managed or customer-managed keys via Key Vault).
- **Data management features**:
  - Soft delete (blobs & containers), versioning, snapshots, immutability policies (WORM — Write Once Read Many) for compliance.
  - Replication: Object Replication for async copy of block blobs between accounts.

### Typical Workflow (Exam + Hands-on)
1. Create a Storage Account: choose subscription/RG, region, performance tier (Standard/Premium), redundancy (LRS/ZRS/GRS/GZRS).
2. Create a Container inside the account; set the public access level (default: Private).
3. Upload blobs: via Portal (drag-drop), Azure Storage Explorer, AzCopy, CLI (`az storage blob upload`), or SDK.
4. Set access tier per blob or use a Lifecycle Management policy to auto-tier/delete over time.
5. Configure access:
   - For internal apps → use Managed Identity + RBAC role assignment.
   - For temporary external sharing → generate a SAS token (set permissions, expiry, IP restriction).
6. Enable data protection: turn on soft delete, versioning, and configure retention period.
7. Monitor: Storage Metrics, Storage Analytics logging, set alerts on capacity/availability.
8. (Optional) Configure Private Endpoint / firewall rules to lock down public access.
9. Decommission: delete blobs/containers, then delete the storage account if no longer needed.

### Exam Tips
- Know minimum storage durations for Cool/Cold/Archive tiers and early-deletion penalty fees.
- Archive tier blobs cannot be read directly — must be rehydrated first (Standard priority = up to 15 hrs, High priority = under 1 hr typically).
- SAS vs Access Keys vs RBAC — exam often tests "least privilege, time-bound access" → answer is SAS (preferably User Delegation SAS).
- GZRS/RA-GZRS is usually the "best durability + read access during regional outage" answer.
- Container access levels: remember default is Private; "Blob" allows anonymous read of blobs but not container listing.

---

## 4. Azure Static Website Hosting (using Storage Account)

### Core Concepts
- A **Storage Account** feature (Static Website) that serves static content (HTML, CSS, JS, images) directly from Blob Storage — no VM/App Service compute needed.
- Automatically creates a special system container named **`$web`** — this is where your site files must be uploaded.
- Provides a **primary endpoint URL** in the form: `https://<accountname>.z[zone].web.core.windows.net/`
- You configure:
  - **Index document name** (e.g., `index.html`) — default page served at root.
  - **Error document path** (e.g., `404.html`) — custom 404 page.
- **Limitations**:
  - Only static content — no server-side code execution (no PHP/ASP.NET/Node backend processing).
  - For dynamic functionality, pair with Azure Functions (serverless backend) or external APIs called via JavaScript.
  - Requires either GPv2 (General Purpose v2) or BlockBlobStorage account type — static website not supported on legacy/general purpose v1 accounts.
- **Custom domain & HTTPS**: To use a custom domain with HTTPS, you typically front the static site with **Azure CDN** or **Azure Front Door**, which also improves global performance via caching/edge locations.
- **CORS**: Configure if the static site needs to call APIs hosted on a different domain.

### Typical Workflow (Exam + Hands-on)
1. Create (or reuse) a Storage Account — must be StorageV2 (general purpose v2) or BlockBlobStorage kind.
2. Enable **Static website** feature (Portal: Storage Account → Data management → Static website → Enabled).
3. Specify Index document name (e.g., `index.html`) and optional Error document path (e.g., `404.html`).
4. Save — Azure auto-creates the `$web` container and generates the **Primary endpoint** URL.
5. Upload your site files (HTML/CSS/JS/images) into the `$web` container via Portal, AzCopy, CLI, or CI/CD pipeline.
6. Test the site using the generated primary endpoint URL.
7. (Optional) Add Azure CDN or Front Door in front of the storage endpoint:
   - Enables custom domain mapping + free/managed HTTPS certificate.
   - Improves performance through edge caching.
8. (Optional) Configure CORS rules on the storage account if the site calls external APIs.
9. (Optional) Add Azure Functions for any dynamic/backend logic, called via client-side JS (Fetch/AJAX).
10. Set up CI/CD (e.g., GitHub Actions / Azure DevOps pipeline) to automate deployment of updated files to `$web` on every commit.
11. Monitor via Storage metrics/logs; optionally enable Application Insights via client-side SDK for usage analytics.

### Exam Tips
- Remember the container name is fixed: **`$web`** — files must go here, not in a custom-named container.
- The static website endpoint is different from the normal blob service endpoint — exam may test you on identifying the correct URL pattern.
- Native static website hosting does NOT support custom domains with HTTPS directly — you need CDN/Front Door for that; this is a common trick question.
- No compute/runtime billing — you only pay for storage + bandwidth (and CDN if used), making this the cheapest hosting option for static sites.
- Static website hosting works only on StorageV2/BlockBlobStorage — not legacy v1 accounts (common gotcha).

---

## Quick Comparison Table (Mental Model for Exam Scenarios)

| Service | Type | When to Choose (exam scenario clue) |
|---|---|---|
| Azure VM | IaaS | "Full OS control", "legacy app", "custom software install", "lift-and-shift" |
| Azure SQL Database | PaaS | "Relational DB, no patching", "scale automatically", "minimize admin overhead" |
| Storage Blob | Object Storage | "Unstructured data", "media/files/backups", "cost-tiered storage" |
| Static Website (Storage) | Serverless static hosting | "Cheapest way to host static HTML/JS site", "no backend code needed" |

---

## General Hands-On Practice Checklist
- [ ] Deploy a VM via Portal AND via Azure CLI — compare experience.
- [ ] Create an NSG rule restricting RDP/SSH to your IP only.
- [ ] Deploy a SQL Database, connect via SSMS/Azure Data Studio, run a query through firewall rules.
- [ ] Configure an Elastic Pool with 2+ databases and observe shared DTU usage.
- [ ] Create a Storage Account, upload blobs, generate and test a SAS URL.
- [ ] Apply a Lifecycle Management rule to move blobs from Hot → Cool → Archive.
- [ ] Enable Static Website hosting, upload a simple `index.html`, and browse the live endpoint.
- [ ] (Stretch) Put Azure CDN in front of the static website and map a custom domain.
