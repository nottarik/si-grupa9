import { useEffect, useRef } from "react";

export function useSubViewBack(isInSubView: boolean, onBack: () => void) {
  const onBackRef = useRef(onBack);
  onBackRef.current = onBack;

  useEffect(() => {
    if (!isInSubView) return;

    // Push a history entry so the browser has something to pop when back is pressed,
    // without changing the visible URL.
    window.history.pushState({ subview: true }, "");

    const handlePopState = () => {
      onBackRef.current();
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, [isInSubView]);
}
