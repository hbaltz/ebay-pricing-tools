# ADR 002 — Frontend: Angular + Capacitor

## Status

Accepted

## Context

The ebay-pricing-tools frontend needs to:

- Provide a pricing search and analysis UI
- Work as a web application (desktop and mobile browsers)
- Be deployable as a **Progressive Web App (PWA)** — installable on mobile home screens, offline-capable
- Potentially be published as a native **Android application** (and optionally iOS in the future)
- Consume the FastAPI backend REST API

Several stacks were evaluated:

| Stack | PWA | Native Android | Learning curve | Maturity |
|-------|-----|---------------|----------------|----------|
| **Angular + Capacitor** | Yes (`@angular/pwa`) | Yes (Capacitor) | Medium | High |
| React + Capacitor | Yes | Yes | Low–Medium | High |
| Vue + Capacitor | Yes | Yes | Low | Medium |
| React Native | Limited web | Yes (native) | Medium | High |
| Flutter | Partial | Yes (native) | High | High |

## Decision

**Angular** as the frontend framework, combined with **Capacitor** as the native runtime bridge.

### Rationale

#### Angular

1. **Opinionated structure**: Angular's enforced conventions (modules, services, dependency injection, routing) make the codebase predictable and maintainable as the tool grows. This matters for a data-heavy tool with multiple views (search, comparison, history, settings).

2. **Built-in PWA support**: The `@angular/pwa` schematic adds a service worker, Web App Manifest, and caching strategy in a single command. Angular's PWA integration is first-class and production-tested.

3. **TypeScript-first**: Angular is built around TypeScript, which pairs naturally with Pydantic-typed responses from the FastAPI backend. Shared type contracts reduce integration bugs.

4. **RxJS for async data**: eBay pricing data involves streams of requests and reactive UI updates (search-as-you-type, polling). RxJS, native to Angular, models these patterns cleanly.

5. **Angular Material / CDK**: Ready-made UI components (tables, forms, dialogs, charts) accelerate building a pricing dashboard.

#### Capacitor

1. **Web-native bridge**: Capacitor wraps the existing Angular web app in a native WebView shell. There is **no separate codebase** for web vs. Android — one Angular app runs everywhere.

2. **PWA + Android from the same build**: The same Angular build artifact is used for the PWA (served from the browser) and the Android APK (wrapped by Capacitor). This minimizes duplication and divergence.

3. **Access to native APIs**: If the Android app later needs camera (barcode scanning for eBay item lookup), push notifications (price alerts), or local storage beyond `localStorage`, Capacitor plugins provide these without rewriting the app.

4. **Ionic ecosystem optional**: Capacitor is maintained by the Ionic team but is framework-agnostic — Angular can be used without committing to Ionic UI components.

5. **Gradual native adoption**: The app can start as a pure PWA, then be wrapped with Capacitor and published to the Play Store when ready, with no architectural change.

### PWA benefits for this tool

- Users can install the tool on their phone home screen without an app store.
- Offline mode can cache recent searches and price history.
- Push notifications (future) can alert users when a tracked item's price drops.

### Android path

1. Angular app is built (`ng build --configuration production`).
2. Capacitor copies the build output into the Android project (`npx cap sync`).
3. Android Studio is used to build and sign the APK/AAB for Play Store distribution.

### Alternatives rejected

- **React + Capacitor**: Functionally equivalent, but Angular's stricter conventions are preferable for a tool that may grow in complexity. The TypeScript-first nature of Angular also aligns better with the typed FastAPI backend.
- **React Native**: Does not produce a PWA. Requires platform-specific code for Android. The web version of the tool would need a separate React web app.
- **Flutter**: Excellent for native apps but Flutter Web is still maturing. The web output is canvas-based, which can hurt accessibility and SEO. Overkill for a tool-style application.

## Consequences

- Frontend: Angular 19+ with standalone components.
- PWA: `@angular/pwa` for service worker and manifest.
- Native: Capacitor 6+ for Android target.
- The frontend will be a separate directory from the Python backend.
- API communication: Angular `HttpClient` with typed Pydantic-derived interfaces.
- The Android app will initially target Play Store internal testing track before public release.
