import React from "react";
import { createRoot } from "react-dom/client";
import LiquidGlass from "liquid-glass-react";

const glassContainer = document.getElementById("hero-liquid-glass");

if (glassContainer) {
  createRoot(glassContainer).render(
    <LiquidGlass
      displacementScale={80}
      blurAmount={0.14}
      saturation={150}
      aberrationIntensity={2}
      elasticity={0.2}
      cornerRadius={32}
      mode="standard"
      padding="0"
      className="hero-liquid-glass"
      style={{
        width: "100%",
        height: "100%",
      }}
    >
      <div className="hero-liquid-glass__surface" />
    </LiquidGlass>,
  );
}
