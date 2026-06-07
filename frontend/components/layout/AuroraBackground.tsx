import Image from "next/image";

const MAP_IMAGE =
  "https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=1600&auto=format&fit=crop";

type Props = {
  showMap?: boolean;
};

/** Fixed cosmic aurora backdrop — stitch purple_aurora. */
export function AuroraBackground({ showMap = true }: Props) {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden>
      <div className="absolute -left-[10%] -top-[10%] h-[40%] w-[40%] animate-pulse-glow rounded-full bg-primary/20 blur-[120px]" />
      <div
        className="absolute -bottom-[10%] -right-[10%] h-[50%] w-[50%] animate-pulse-glow rounded-full bg-secondary/10 blur-[150px]"
        style={{ animationDelay: "2s" }}
      />
      {showMap ? (
        <div
          className="absolute inset-0 opacity-20"
          style={{
            maskImage:
              "linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6) 50%, rgba(0,0,0,0) 100%)",
            WebkitMaskImage:
              "linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6) 50%, rgba(0,0,0,0) 100%)",
          }}
        >
          <Image
            src={MAP_IMAGE}
            alt=""
            fill
            className="object-cover"
            unoptimized
            priority
          />
        </div>
      ) : null}
    </div>
  );
}
