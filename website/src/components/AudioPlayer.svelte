<script>
  import { createEventDispatcher } from "svelte"

  export let src
  export let title
  export let artist

  let time = 0
  let duration = 0
  let paused = true

  $: broadcastPausedChange(paused)

  const eventDispatcher = createEventDispatcher()

  function broadcastTimeChange(time) {
    eventDispatcher("change", time)
  }
  function broadcastPausedChange(paused) {
    eventDispatcher("paused", paused)
  }

  function format(time) {
    if (isNaN(time)) return "..."

    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)

    return `${minutes}:${seconds < 10 ? `0${seconds}` : seconds}`
  }
</script>

<div class="player" class:paused>
  <audio
    {src}
    bind:currentTime={time}
    bind:duration
    bind:paused
    preload="metadata"
    on:ended={() => {
      time = 0
    }}
  />

  <button
    class="play"
    aria-label={paused ? "play" : "pause"}
    on:click={() => (paused = !paused)}
  />

  <div class="info">
    <div class="description">
      <strong>{title}</strong> /
      <span>{artist}</span>
    </div>

    <div class="time">
      <span>{format(time)}</span>
      <div
        class="slider"
        on:pointerdown={(e) => {
          const div = e.currentTarget

          function seek(e) {
            const { left, width } = div.getBoundingClientRect()

            let p = (e.clientX - left) / width
            if (p < 0) p = 0
            if (p > 1) p = 1

            time = p * duration
            broadcastTimeChange(time)
          }

          seek(e)

          window.addEventListener("pointermove", seek)

          window.addEventListener(
            "pointerup",
            () => {
              window.removeEventListener("pointermove", seek)
            },
            {
              once: true,
            }
          )
        }}
      >
        <div class="progress" style="--progress: {time / duration}%" />
      </div>
      <span>{duration ? format(duration) : "--:--"}</span>
    </div>
  </div>
</div>

<style>
  .player {
    display: grid;
    grid-template-columns: 2.5em 1fr;
    align-items: center;
    gap: 1em;
    padding: 0.5em 1em 0.5em 0.5em;
    border-radius: 2em;
    transition: filter 0.2s;
    user-select: none;
    width: 100%;
  }

  .player:not(.paused) {
    filter: drop-shadow(0.5em 0.5em 1em rgba(0, 0, 0, 0.1));
  }

  button {
    width: 100%;
    aspect-ratio: 1;
    background-repeat: no-repeat;
    background-position: 50% 50%;
    border-radius: 50%;
  }

  [aria-label="pause"] {
    background-image: url(./pause.svg);
  }

  [aria-label="play"] {
    background-image: url(./play.svg);
  }

  .info {
    overflow: hidden;
  }

  .description {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
  }

  .time {
    display: flex;
    align-items: center;
    gap: 0.5em;
  }

  .time span {
    font-size: 0.7em;
  }

  .slider {
    flex: 1;
    height: 0.5em;
    border-radius: 0.5em;
    overflow: hidden;
  }

  .progress {
    width: calc(100 * var(--progress));
    height: 100%;
    background: var(--accent);
  }
</style>
