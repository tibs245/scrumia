# Views is an explicit choice

*Refusal.* A View-based widget, Activity with an XML layout, `ViewBinding`,
`RecyclerView` with a custom `ViewHolder`, or any other `android.view.View` or
`android.widget.*` artefact is refused unless the PR states the justification for
choosing Views over the Compose default.

## What is refused

A new View-based surface written as if it were the default. Three shapes this
takes:

```kotlin
// ❌ a new screen written as a View — no justification offered
class ProductListActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_product_list)
    }
}
```

```xml
<!-- ❌ the layout file the activity inflates -->
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/products"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</LinearLayout>
```

```kotlin
// ❌ a custom View — no Compose equivalent reached for first
class ProductCardView : ConstraintLayout {
    // ...
}
```

A project that adopts Compose by default reaches for the Compose equivalents
(`ProductListScreen` as a Composable, `LazyColumn` for the list, `Card` for the
card), and a Views surface is the answer only when one of the justifications
below applies.

## What justifies the choice

A stated justification in the PR, naming one of:

- **Legacy migration.** An existing screen or feature is being rewritten to use
  Material 3 styling without rewriting its View-based architecture. The
  justification names the screen or feature and references the migration plan.
- **View-only third-party dependency.** A library exposes a `View` and no
  Compose wrapper — a charting library, a camera preview, a maps overlay. The
  justification names the dependency and the missing Compose API.
- **Performance constraint.** A measured, profiled bottleneck that Compose cannot
  yet clear for the surface in question. The justification carries the profile and
  the threshold Compose failed to meet.

Anything outside these three — preference, familiarity, "the team knows XML
better" — is a refusal. The default is the answer the project reaches for first;
a choice against it is a justified exception.

## What is written instead

A greenfield surface is a Composable, period. The Compose default is governed by
[`compose-default`](compose-default.md). A Views surface is the answer only when
one of the three justifications applies, and only for the file or feature that
needs it; a single View-based widget in an otherwise-Compose surface is the common
case (third-party View integration), and the rest of the surface stays Compose.

## Why

Compose is Google's stated default for new Android UI. A project that does not
state "Views is the exception, not the default" produces a codebase where each
screen reflects the developer's background, not the project's rule. The
justification is the discipline that catches a View-based surface before it lands
and asks the author whether Compose was considered and on what ground it lost.

## Sources complémentaires

- [`https://developer.android.com/jetpack/compose/migration`](https://developer.android.com/jetpack/compose/migration) — Compose migration strategies.
- [`https://developer.android.com/jetpack/compose/interop`](https://developer.android.com/jetpack/compose/interop) — Compose / Views interoperability, for the third-party-dependency case.
