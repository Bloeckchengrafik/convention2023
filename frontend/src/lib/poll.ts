import { onMount } from 'svelte';

export function poll(fn: () => void, ms: number) {
    onMount(() => {
        const interval = setInterval(fn, ms);
        fn();

        return () => clearInterval(interval);
    });
}