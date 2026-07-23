(() => {
  const initialiseRedShelf = () => {
    document.querySelectorAll(".copy-citation").forEach((button) => {
      if (button.dataset.ready === "true") return;
      button.dataset.ready = "true";

      button.addEventListener("click", async () => {
        const citation = button.dataset.citation;
        if (!citation) return;

        const original = button.textContent;
        try {
          await navigator.clipboard.writeText(citation);
          button.textContent = "Citation copied";
          button.setAttribute("aria-label", "Citation copied to clipboard");
        } catch {
          const textArea = document.createElement("textarea");
          textArea.value = citation;
          textArea.style.position = "fixed";
          textArea.style.opacity = "0";
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand("copy");
          textArea.remove();
          button.textContent = "Citation copied";
        }

        window.setTimeout(() => {
          button.textContent = original;
          button.setAttribute("aria-label", "Copy citation");
        }, 2200);
      });
    });

    document.querySelectorAll("[data-open-search]").forEach((button) => {
      if (button.dataset.ready === "true") return;
      button.dataset.ready = "true";
      button.addEventListener("click", () => {
        const searchToggle = document.querySelector("[data-md-toggle='search']");
        if (searchToggle) searchToggle.checked = true;
        window.setTimeout(() => {
          document.querySelector(".md-search__input")?.focus();
        }, 80);
      });
    });

    document.querySelectorAll("[data-current-year]").forEach((node) => {
      node.textContent = new Date().getFullYear();
    });
  };

  if (typeof document$ !== "undefined") {
    document$.subscribe(initialiseRedShelf);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseRedShelf);
  } else {
    initialiseRedShelf();
  }
})();
