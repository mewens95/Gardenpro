-- GardenPro database setup
-- Run this ONCE in Supabase > SQL Editor.
-- It creates the tables and security rules used by the GardenPro website.

create extension if not exists pgcrypto;

create table if not exists public.customers (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  address text,
  phone text,
  email text,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  customer_id uuid not null references public.customers(id) on delete cascade,
  title text not null,
  date date not null,
  repeat text not null default 'One-off',
  price numeric(12,2) not null default 0,
  done boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.quotes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  customer_id uuid not null references public.customers(id) on delete cascade,
  title text not null,
  amount numeric(12,2) not null default 0,
  status text not null default 'Draft',
  created_at timestamptz not null default now()
);

create table if not exists public.invoices (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  customer_id uuid not null references public.customers(id) on delete cascade,
  title text not null,
  amount numeric(12,2) not null default 0,
  status text not null default 'Unpaid',
  created_at timestamptz not null default now()
);

alter table public.customers enable row level security;
alter table public.jobs enable row level security;
alter table public.quotes enable row level security;
alter table public.invoices enable row level security;

drop policy if exists "customers own rows" on public.customers;
create policy "customers own rows" on public.customers for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "jobs own rows" on public.jobs;
create policy "jobs own rows" on public.jobs for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "quotes own rows" on public.quotes;
create policy "quotes own rows" on public.quotes for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "invoices own rows" on public.invoices;
create policy "invoices own rows" on public.invoices for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

create index if not exists customers_user_id_idx on public.customers(user_id);
create index if not exists jobs_user_id_date_idx on public.jobs(user_id,date);
create index if not exists quotes_user_id_idx on public.quotes(user_id);
create index if not exists invoices_user_id_idx on public.invoices(user_id);
