# Coroutines, structured concurrency, scopes, dispatchers, cancellation, Flow

*Refusal.* Unstructured concurrency (`GlobalScope.launch` outside the bootstrap);
swallowed `CancellationException`; a `Flow.collect` outside a scope; a `Dispatcher`
hard-coded at the call site. Each one is a contract the Kotlin coroutines guide
documents and that the code silently breaks.

## What is refused

```kotlin
// ❌ GlobalScope.launch has no parent; cancellation does not reach it; leaks past the screen
fun onCleared() {
    GlobalScope.launch { repository.sync() }   // survives the ViewModel; survives the screen
}

// ❌ the catch swallows CancellationException, which is how structured cancellation propagates
runCatching {
    val data = fetchFromNetwork()
    persist(data)
}

// ❌ Flow.collect is itself a suspending function and needs a scope; a bare block has none
fun watch() {
    repository.updates().collect { render(it) }   // what scope owns this?
}

// ❌ Dispatchers.Main is hard-coded; the test cannot substitute Main, the production code cannot switch threads
suspend fun load(): Data = withContext(Dispatchers.Main) { repository.load() }
```

The first case compiles today and is the failure mode this rule names. The Kotlin
coroutines guide is explicit: `GlobalScope.launch` is for long-lived, application-wide
work — exactly the cases where cancellation is the wrong default. Using it for a
ViewModel-scoped job is the same defect with a longer lifetime: the job outlives the
screen, the repository outlives the process, and the next reader has to prove to
themselves that nothing else holds a reference.

The second case compiles today and the tests pass; it is also the failure mode
`kotlinx.coroutines` documents as the wrong default. The
[`runCatching` reference](https://kotlinlang.org/docs/coroutines-guide.html) is
explicit: `CancellationException` is the channel through which structured cancellation
propagates, and `runCatching` catches it the same way it catches every other
`Throwable`. The cancellation stops reaching up; the parent never learns the child has
given up; the job that should have been cancelled is the one that finished.

The third case is the same defect from a different angle. `Flow.collect` is itself a
suspending function — to call it, you need a `CoroutineScope`. A bare block on a
member function of a non-suspending class is not in a scope; the call is unreachable
and the compiler says so. The variant that compiles — `lifecycleScope.launch { ... }`
or `viewModelScope.launch { ... }` — names who owns the work.

The fourth case is the wrong seam. The Kotlin coroutines guide recommends `Dispatchers`
be injected — passed in or held in a constructor — so a test can substitute
`UnconfinedTestDispatcher` and the production code can switch dispatchers for an
upstream that demands a different thread pool. Hard-coding `Dispatchers.Main` couples
the function to the platform and breaks the test.

## What is written instead

**Structured concurrency, scoped lifetimes, cooperative cancellation.** From the
[coroutines guide](https://kotlinlang.org/docs/coroutines-guide.html) and the
[structured concurrency reference](https://kotlinlang.org/docs/coroutines-guide.html):

```kotlin
// ✅ the job is owned by the ViewModel's scope; cancellation follows the ViewModel
class OrderViewModel(private val repository: OrderRepository) : ViewModel() {
    fun sync() {
        viewModelScope.launch {
            val data = repository.sync()
            _state.value = data
        }
    }
}

// ✅ `try { ... } catch (e: Exception)` rethrows CancellationException; structured cancellation survives
try {
    val data = fetchFromNetwork()
    persist(data)
} catch (e: CancellationException) {
    throw e                         // never swallow
} catch (e: IOException) {
    log.error(e) { "fetch failed" }
    _state.value = State.Error(e)
}

// ✅ Flow is collected in a scope; the lifetime is explicit
class OrderViewModel(...) : ViewModel() {
    init {
        viewModelScope.launch {
            repository.updates().collect { render(it) }
        }
    }
}

// ✅ Dispatchers injected; production and tests pass the same shape
class LoadOrderUseCase(
    private val repository: OrderRepository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.Default,
) {
    suspend fun load(id: OrderId): Order = withContext(dispatcher) {
        repository.load(id)
    }
}
```

**`Flow` cold by default; `StateFlow` / `SharedFlow` only at the seam.** A `Flow` is
cold: each collector runs the upstream. `StateFlow` and `SharedFlow` are hot: the
upstream runs once, the value is shared. The two are not interchangeable:

```kotlin
// ✅ cold Flow, one collector at a time
fun orders(): Flow<List<Order>> = repository.observeOrders()

// ✅ StateFlow at the UI seam, where a hot, conflated stream is what the screen reads
class OrderViewModel(...) : ViewModel() {
    private val _state = MutableStateFlow(State.Loading)
    val state: StateFlow<State> = _state.asStateFlow()
}
```

## Why

The coroutines guide calls structured concurrency "the default and recommended
approach" because it makes the lifetime of work match the lifetime of the code that
started it. A job no parent can cancel is a leak — not in the memory sense, but in the
behavioural sense: the job's effect on the world outlives the contract that started
it. `GlobalScope` is the one escape the language offers, and the guide names it for
exactly the cases where cancellation is wrong (an application-wide heartbeat, a
process-wide observer). Every other case has a scope that already exists.

`CancellationException` is the channel through which structured cancellation
propagates. A catch that does not distinguish it from any other `Throwable` cuts the
channel, and the cancellation that was supposed to stop the work is the cancellation
that was caught. The Kotlin coroutines API documents this twice — once in
`runCatching` and once in the `kotlinx.coroutines` exception handling reference — and
the cost of skipping it is the cost of every job that should have stopped but did not.

A `Flow.collect` without a scope is unreachable, and the compiler says so. The
reachable shape (`launch { collect { } }`) names who owns the work, and the lifetime
of the work follows the lifetime of the scope. Hard-coding `Dispatchers.Main` is the
same defect on the threading axis: the function's contract is "run on the platform
thread", and the test cannot honour that contract without binding the platform thread
to itself.

## Sources complémentaires

- Kotlin docs — [Coroutines guide](https://kotlinlang.org/docs/coroutines-guide.html) — structured concurrency, scopes, dispatchers, cancellation, Flow. Version pin: **Kotlin coroutines**.
- Kotlin docs — [Coroutine exceptions handling](https://kotlinlang.org/docs/exception-handling.html) — why `CancellationException` is rethrown, not swallowed. Version pin: **Kotlin coroutines**.
- Kotlin docs — [Asynchronous Flow](https://kotlinlang.org/docs/flow.html) — cold `Flow`, hot `StateFlow` / `SharedFlow`, the seam where hot is the right choice. Version pin: **Kotlin coroutines**.
