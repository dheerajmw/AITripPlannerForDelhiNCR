import { Footprints } from "lucide-react";

type Props = {
  minutes: number;
};

export function TravelLeg({ minutes }: Props) {
  return (
    <div className="relative py-6 pl-12">
      <div className="travel-line-dashed" aria-hidden />
      <div className="relative z-10 flex items-center gap-3 text-secondary">
        <div className="flex h-8 w-8 items-center justify-center rounded-full border border-secondary bg-surface-container">
          <Footprints className="h-[18px] w-[18px]" aria-hidden />
        </div>
        <span className="text-body-sm font-bold">{minutes} min walk to next stop</span>
      </div>
    </div>
  );
}
