# GardenPro release checklist

## Launch price

- Subscription price: **£6.99/month**
- Recommended launch offer: **7-day free trial**
- Do not hard-code a Google Play product ID until the product has been created in Play Console.

## Completed in the repository

- Capacitor app ID: `com.gardenpro.app`
- App name: `GardenPro`
- Reproducible Android AAB build script: `build-mobile.mjs`
- `npm run android:build` now runs that build script
- Supabase schema includes the `expenses` table with row-level security

## Still required before public launch

### 1. Supabase

Run the latest `supabase-schema.sql` in the Supabase SQL Editor so the `expenses` table exists in the live database.

### 2. Google Play developer account

- Register the full-distribution Android developer account.
- Complete identity/contact verification.
- Register the GardenPro package name `com.gardenpro.app` when Play Console makes that available/required.

### 3. Android release build

- Generate the Android project with `npm run android:build` on a machine with Node, JDK and Android SDK installed.
- Configure the release signing key/keystore.
- Build and inspect the release `.aab`.
- Test the release build on a real Android phone.

### 4. Google Play subscription

Create a subscription product in Play Console:

- Product: GardenPro monthly
- Price: £6.99/month
- Base plan: monthly auto-renewing
- Optional introductory offer: 7-day free trial

The final product ID must be recorded here after it is created. Example placeholder only: `gardenpro_monthly`.

### 5. In-app billing integration

Integrate Google Play Billing into the Android app and connect it to the GardenPro account entitlement. The implementation must use a currently supported Google Play Billing Library version; **do not use older Capacitor billing plugins that depend on Billing Library 7** for this new app.

The app must:

- Show the £6.99 subscription screen.
- Launch Google Play's purchase flow.
- Acknowledge purchases correctly.
- Restore/check an existing subscription on login/app start.
- Handle cancelled, grace-period, on-hold and expired states.
- Prevent premium access after the entitlement expires.

### 6. Store/legal setup

- Privacy policy URL
- Support/contact details
- App description and screenshots
- Data safety declaration
- Content rating
- App icon and feature graphic
- Pricing/subscription disclosures

### 7. Testing

Test at minimum:

- New account
- Login/logout
- Customer creation/edit/delete
- Job creation/edit/delete
- Calendar
- Quotes
- Invoices
- Expenses
- Profile/business details
- Offline/poor connection behaviour
- Subscription purchase
- Subscription restore
- Subscription cancellation/expiry handling

## Important pricing note

£6.99/month is the agreed GardenPro launch price. Pricing can be changed later for new customers without changing the app's core features.
