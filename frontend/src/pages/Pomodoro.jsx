import { useEffect, useMemo, useRef, useState } from 'react';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { Play, Pause, RotateCcw, Clock, Bell } from 'lucide-react';

export default function Pomodoro() {
  const [minutes, setMinutes] = useState(25); // default 25 mins
  const [secondsLeft, setSecondsLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [label, setLabel] = useState('Focus');
  const intervalRef = useRef(null);
  const bellRef = useRef(null);

  // keep seconds in sync when minute preset changes (only when not running)
  useEffect(() => {
    if (!isRunning) {
      const clamped = Math.min(60, Math.max(1, minutes));
      setMinutes(clamped);
      setSecondsLeft(clamped * 60);
    }
  }, [minutes, isRunning]);

  useEffect(() => {
    if (!isRunning) return;
    intervalRef.current = setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= 1) {
          clearInterval(intervalRef.current);
          setIsRunning(false);
          try { bellRef.current?.play?.(); } catch {}
          return 0;
        }
        return s - 1;
      });
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, [isRunning]);

  const totalSeconds = useMemo(() => Math.max(60, Math.min(60 * 60, minutes * 60)), [minutes]);
  const progress = useMemo(() => 1 - secondsLeft / totalSeconds, [secondsLeft, totalSeconds]);

  const display = useMemo(() => {
    const m = Math.floor(secondsLeft / 60).toString().padStart(2, '0');
    const s = Math.floor(secondsLeft % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }, [secondsLeft]);

  const start = () => {
    if (secondsLeft <= 0) setSecondsLeft(totalSeconds);
    setIsRunning(true);
  };
  const pause = () => setIsRunning(false);
  const reset = () => {
    setIsRunning(false);
    setSecondsLeft(totalSeconds);
  };

  const setPreset = (m, newLabel) => {
    setLabel(newLabel);
    setIsRunning(false);
    setMinutes(m);
    setSecondsLeft(m * 60);
  };

  const ringSize = 180;
  const stroke = 10;
  const radius = (ringSize - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference * (1 - progress);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Pomodoro</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Focused work timer with presets up to 60 minutes</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card flex items-center justify-center">
          <div className="text-center">
            <div className="mx-auto mb-6 relative" style={{ width: ringSize, height: ringSize }}>
              <svg width={ringSize} height={ringSize}>
                <circle
                  cx={ringSize / 2}
                  cy={ringSize / 2}
                  r={radius}
                  stroke="currentColor"
                  className="text-gray-200 dark:text-gray-700"
                  strokeWidth={stroke}
                  fill="none"
                />
                <circle
                  cx={ringSize / 2}
                  cy={ringSize / 2}
                  r={radius}
                  stroke="url(#grad)"
                  strokeWidth={stroke}
                  fill="none"
                  strokeDasharray={circumference}
                  strokeDashoffset={dashOffset}
                  strokeLinecap="round"
                  transform={`rotate(-90 ${ringSize / 2} ${ringSize / 2})`}
                />
                <defs>
                  <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#0ea5e9" />
                    <stop offset="100%" stopColor="#a855f7" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-sm text-gray-500 dark:text-gray-400">{label}</div>
                <div className="text-4xl font-bold text-gray-900 dark:text-white">{display}</div>
              </div>
            </div>

            <div className="flex items-center justify-center gap-3">
              {isRunning ? (
                <Button onClick={pause} className="min-w-[120px]">
                  <Pause className="mr-2" size={16} /> Pause
                </Button>
              ) : (
                <Button onClick={start} className="min-w-[120px]">
                  <Play className="mr-2" size={16} /> Start
                </Button>
              )}
              <Button variant="secondary" onClick={reset}>
                <RotateCcw className="mr-2" size={16} /> Reset
              </Button>
            </div>
            <audio ref={bellRef} src="data:audio/mp3;base64,//uQZAAAAAAAAAAAAAAAAAAAA..." preload="auto" />
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Presets & Settings</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
            <Button variant="secondary" onClick={() => setPreset(25, 'Focus')}><Clock className="mr-2" size={16} />25:00</Button>
            <Button variant="secondary" onClick={() => setPreset(5, 'Break')}><Bell className="mr-2" size={16} />5:00</Button>
            <Button variant="secondary" onClick={() => setPreset(15, 'Break')}><Bell className="mr-2" size={16} />15:00</Button>
            <Button variant="secondary" onClick={() => setPreset(45, 'Focus')}><Clock className="mr-2" size={16} />45:00</Button>
            <Button variant="secondary" onClick={() => setPreset(60, 'Focus')}><Clock className="mr-2" size={16} />60:00</Button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Custom minutes (1-60)</label>
            <div className="flex items-center gap-3">
              <Input
                type="number"
                min={1}
                max={60}
                value={minutes}
                onChange={(e) => setMinutes(Number(e.target.value || 1))}
                className="max-w-[140px]"
              />
              <Button variant="secondary" onClick={() => setPreset(Math.min(60, Math.max(1, minutes)), 'Custom')}>Apply</Button>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Timer caps at 60 minutes.</p>
          </div>
        </div>
      </div>
    </div>
  );
}


