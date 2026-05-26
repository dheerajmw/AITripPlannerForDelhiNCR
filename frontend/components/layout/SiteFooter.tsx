export function SiteFooter() {
  return (
    <footer className="relative mt-16 hidden border-t border-outline-variant bg-surface-container-lowest py-8 md:flex md:flex-row md:items-center md:justify-between md:px-container-desktop">
      <div className="flex flex-col gap-1">
        <span className="text-lg font-bold text-on-surface">Delhi AI Travel</span>
        <p className="text-sm text-on-surface-variant">
          © {new Date().getFullYear()} Delhi AI Travel. Estimates are approximate.
        </p>
      </div>
      <nav className="flex gap-6">
        {["Terms", "Privacy", "Support"].map((label) => (
          <span
            key={label}
            className="cursor-default font-mono text-sm text-on-surface-variant"
          >
            {label}
          </span>
        ))}
      </nav>
    </footer>
  );
}
