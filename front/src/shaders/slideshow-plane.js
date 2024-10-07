export const vertexShader = `
    precision mediump float;
    // default mandatory variables
    attribute vec3 aVertexPosition;
    attribute vec2 aTextureCoord;
    uniform mat4 uMVMatrix;
    uniform mat4 uPMatrix;
    // varyings : notice we've got 3 texture coords varyings
    // one for the displacement texture
    // one for our visible texture
    // and one for the upcoming texture
    varying vec3 vVertexPosition;
    varying vec2 vTextureCoord;
    varying vec2 vActiveTextureCoord;
    varying vec2 vNextTextureCoord;
    // textures matrices
    uniform mat4 activeTexMatrix;
    uniform mat4 nextTexMatrix;
    // custom uniforms
    uniform float uTransitionTimer;
    void main() {
        gl_Position = uPMatrix * uMVMatrix * vec4(aVertexPosition, 1.0);
        // varyings
        vTextureCoord = aTextureCoord;
        vActiveTextureCoord = (activeTexMatrix * vec4(aTextureCoord, 0.0, 1.0)).xy;
        vNextTextureCoord = (nextTexMatrix * vec4(aTextureCoord, 0.0, 1.0)).xy;
        vVertexPosition = aVertexPosition;
    }
`;

export const fragmentShader = `
    precision mediump float;
    varying vec3 vVertexPosition;
    varying vec2 vTextureCoord;
    varying vec2 vActiveTextureCoord;
    varying vec2 vNextTextureCoord;
    // custom uniforms
    uniform float uTransitionTimer;
    // our textures samplers
    // notice how it matches the sampler attributes of the textures we created dynamically
    uniform sampler2D activeTex;
    uniform sampler2D nextTex;
    uniform sampler2D displacement;
    void main() {
        // our displacement texture
        vec4 displacementTexture = texture2D(displacement, vTextureCoord);
        // slides transitions based on displacement and transition timer
        vec2 firstDisplacementCoords = vActiveTextureCoord + displacementTexture.r * ((cos((uTransitionTimer + 90.0) / (90.0 / 3.141592)) + 1.0) / 1.25);
        vec4 firstDistortedColor = texture2D(activeTex, vec2(vActiveTextureCoord.x, firstDisplacementCoords.y));
        // same as above but we substract the effect
        vec2 secondDisplacementCoords = vNextTextureCoord - displacementTexture.r * ((cos(uTransitionTimer / (90.0 / 3.141592)) + 1.0) / 1.25);
        vec4 secondDistortedColor = texture2D(nextTex, vec2(vNextTextureCoord.x, secondDisplacementCoords.y));
        // mix both texture
        vec4 finalColor = mix(firstDistortedColor, secondDistortedColor, 1.0 - ((cos(uTransitionTimer / (90.0 / 3.141592)) + 1.0) / 2.0));
        // handling premultiplied alpha
        finalColor = vec4(finalColor.rgb * finalColor.a, finalColor.a);
        gl_FragColor = finalColor;
    }
`;
