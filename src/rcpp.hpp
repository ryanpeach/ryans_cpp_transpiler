// RCPP Header Definitions
// TODO: Replace with include <rcpp>
// These are defined into existence but do nothing
#define mut

// These are simple renames
#define dumb(X) X*
#define ref(X) X&
#define rref(X) X&&
#define univref(X) X&&
#define deref(X) *X
#define addr(X) &X
#define make_dumb(X) new X
#define shared(X) std::shared_ptr<X>
#define make_shared(X) std::make_shared(X)
#define weak(X) std::weak_ptr<X>
#define unique(X) std::unique_ptr<X>
#define make_unique(X) std::make_unique(X)
// END RCPP Header Definitions
