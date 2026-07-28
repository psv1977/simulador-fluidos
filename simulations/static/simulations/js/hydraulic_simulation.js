document.addEventListener("DOMContentLoaded", () => {
    // =====================================================
    // Campos de entrada
    // =====================================================

    const diameterInput = document.getElementById("id_diameter_m");
    const flowRateInput = document.getElementById("id_flow_rate_m3_s");
    const densityInput = document.getElementById("id_density_kg_m3");
    const viscosityInput = document.getElementById(
        "id_dynamic_viscosity_pa_s"
    );

    // =====================================================
    // Valores mostrados en la interfaz
    // =====================================================

    const diameterValue = document.getElementById("diameter-value");

    const pipeDiameterValue = document.getElementById(
        "pipe-diameter-value"
    );

    const velocityProfileLabel = document.getElementById(
        "velocity-profile-label"
    );

    const areaResult = document.getElementById("area-result");
    const velocityResult = document.getElementById("velocity-result");
    const reynoldsResult = document.getElementById("reynolds-result");

    const flowRegimeResult = document.getElementById(
        "flow-regime-result"
    );

    // =====================================================
    // Canvas
    // =====================================================

    const pipeCanvas = document.getElementById("pipe-canvas");

    const pipeContext = pipeCanvas
        ? pipeCanvas.getContext("2d")
        : null;

    if (
        !diameterInput ||
        !flowRateInput ||
        !densityInput ||
        !viscosityInput ||
        !pipeCanvas ||
        !pipeContext
    ) {
        console.error(
            "FluidaLab: faltan elementos necesarios para iniciar la simulación."
        );
        return;
    }

    // =====================================================
    // Conversión y formato numérico
    // =====================================================

    function parseNumericValue(input) {
        if (!input || typeof input.value !== "string") {
            return NaN;
        }

        return Number.parseFloat(
            input.value.trim().replace(",", ".")
        );
    }

    function formatNumber(value, decimals) {
        if (!Number.isFinite(value)) {
            return "—";
        }

        return value.toLocaleString("es-CL", {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals,
        });
    }

    // =====================================================
    // Régimen de flujo
    // =====================================================

    function classifyFlowRegime(reynoldsNumber) {
        if (reynoldsNumber < 2300) {
            return "Laminar";
        }

        if (reynoldsNumber < 4000) {
            return "Transicional";
        }

        return "Turbulento";
    }

    // =====================================================
    // Perfil de velocidades
    // =====================================================

    function getProfileFactor(
        relativePosition,
        flowRegime
    ) {
        const radialPosition = Math.min(
            Math.abs(relativePosition),
            1
        );

        /*
         * LAMINAR
         *
         * Perfil parabólico:
         * u / umax = 1 - (r/R)^2
         */
        const laminarFactor = Math.max(
            1 - Math.pow(radialPosition, 2),
            0
        );

        /*
         * TURBULENTO
         *
         * Aproximación mediante ley de potencia 1/7.
         * Produce un perfil más plano en el núcleo
         * y una caída fuerte cerca de las paredes.
         */
        const turbulentFactor = Math.pow(
            Math.max(1 - radialPosition, 0),
            1 / 7
        );

        if (flowRegime === "Laminar") {
            return laminarFactor;
        }

        if (flowRegime === "Transicional") {
            return (
                0.5 * laminarFactor +
                0.5 * turbulentFactor
            );
        }

        return turbulentFactor;
    }

    // =====================================================
    // Limpieza de resultados
    // =====================================================

    function clearResults() {
        if (areaResult) {
            areaResult.textContent = "—";
        }

        if (velocityResult) {
            velocityResult.textContent = "—";
        }

        if (reynoldsResult) {
            reynoldsResult.textContent = "—";
        }

        if (flowRegimeResult) {
            flowRegimeResult.textContent = "—";
        }

        if (velocityProfileLabel) {
            velocityProfileLabel.textContent = "—";
        }

        pipeContext.clearRect(
            0,
            0,
            pipeCanvas.width,
            pipeCanvas.height
        );
    }

    // =====================================================
    // Escala visual del diámetro
    // =====================================================

    function calculatePipeHeight(diameter) {
        const minimumDiameter = Number.parseFloat(
            diameterInput.min
        );

        const maximumDiameter = Number.parseFloat(
            diameterInput.max
        );

        if (
            !Number.isFinite(minimumDiameter) ||
            !Number.isFinite(maximumDiameter) ||
            maximumDiameter <= minimumDiameter
        ) {
            return 100;
        }

        const normalizedDiameter =
            (diameter - minimumDiameter) /
            (maximumDiameter - minimumDiameter);

        const boundedDiameter = Math.min(
            Math.max(normalizedDiameter, 0),
            1
        );

        /*
         * Escala visual relativa.
         * El diámetro mínimo continúa siendo visible.
         */
        const minimumPipeHeight = 55;
        const maximumPipeHeight = 175;

        return (
            minimumPipeHeight +
            boundedDiameter *
                (maximumPipeHeight - minimumPipeHeight)
        );
    }

    // =====================================================
    // Flecha individual
    // =====================================================

    function drawArrow(context, startX, y, length) {
        const endX = startX + length;
        const arrowSize = 7;

        context.beginPath();
        context.moveTo(startX, y);
        context.lineTo(endX, y);
        context.stroke();

        context.beginPath();
        context.moveTo(endX, y);

        context.lineTo(
            endX - arrowSize,
            y - arrowSize / 2
        );

        context.lineTo(
            endX - arrowSize,
            y + arrowSize / 2
        );

        context.closePath();
        context.fill();
    }

    // =====================================================
    // Color y nombre visual del régimen
    // =====================================================

    function getRegimeStyle(flowRegime) {
        if (flowRegime === "Laminar") {
            return {
                color: "#0878b5",
                fluidColor: "#d9eff8",
            };
        }

        if (flowRegime === "Transicional") {
            return {
                color: "#a15c00",
                fluidColor: "#fff0d5",
            };
        }

        return {
            color: "#a12b2b",
            fluidColor: "#f8dddd",
        };
    }

    // =====================================================
    // Dibujo longitudinal
    // =====================================================

    function drawPipeVisualization(
        diameter,
        velocity,
        flowRegime
    ) {
        const context = pipeContext;
        const canvasWidth = pipeCanvas.width;
        const canvasHeight = pipeCanvas.height;

        context.clearRect(
            0,
            0,
            canvasWidth,
            canvasHeight
        );

        const pipeHeight = calculatePipeHeight(diameter);

        /*
         * Tubería más corta y desplazada hacia la izquierda 
         */
        const pipeWidth = canvasWidth * 0.58;
        const pipeLeft = canvasWidth * 0.02;
        const pipeRight = pipeLeft + pipeWidth;

        const pipeTop =
            (canvasHeight - pipeHeight) / 2;

        const pipeBottom = pipeTop + pipeHeight;
        const pipeCenterY = canvasHeight / 2;
        const pipeRadius = pipeHeight / 2;

        const regimeStyle = getRegimeStyle(flowRegime);

        // ---------------------------------------------
        // Interior del ducto
        // ---------------------------------------------

        context.fillStyle = regimeStyle.fluidColor;

        context.fillRect(
            pipeLeft,
            pipeTop,
            pipeWidth,
            pipeHeight
        );

        // ---------------------------------------------
        // Paredes superior e inferior
        // ---------------------------------------------

        context.strokeStyle = "#425a65";
        context.lineWidth = 8;
        context.lineCap = "round";

        context.beginPath();
        context.moveTo(pipeLeft, pipeTop);
        context.lineTo(pipeRight, pipeTop);
        context.stroke();

        context.beginPath();
        context.moveTo(pipeLeft, pipeBottom);
        context.lineTo(pipeRight, pipeBottom);
        context.stroke();

        // ---------------------------------------------
        // Línea central
        // ---------------------------------------------

        context.setLineDash([8, 8]);
        context.strokeStyle = "#8aa3ad";
        context.lineWidth = 1;

        context.beginPath();
        context.moveTo(pipeLeft, pipeCenterY);
        context.lineTo(pipeRight, pipeCenterY);
        context.stroke();

        context.setLineDash([]);

        // ---------------------------------------------
        // Flechas del perfil
        // ---------------------------------------------

        context.strokeStyle = regimeStyle.color;
        context.fillStyle = regimeStyle.color;
        context.lineWidth = 2;

        /*
         * Número impar para que exista una flecha
         * exactamente en el eje central.
         */
        const arrowCount = 17;

        /*
         * Longitud máxima reducida para que el perfil
         * quede dentro del ducto.
         */
        const maximumArrowLength = pipeWidth * 0.38;

        /*
         * El perfil muestra la distribución espacial.
         * La velocidad real se informa numéricamente;
         * no se usa para deformar demasiado el dibujo.
         */
        const velocityScale = 1;

        const arrowStartX = pipeLeft + pipeWidth * 0.12;

        for (
            let index = 0;
            index < arrowCount;
            index += 1
        ) {
            const fraction =
                index / (arrowCount - 1);

            /*
             * Primera y última posición coinciden
             * con las paredes.
             */
            const y =
                pipeTop +
                fraction * pipeHeight;

            const relativePosition =
                (y - pipeCenterY) /
                Math.max(pipeRadius, 1);

            const profileFactor = getProfileFactor(
                relativePosition,
                flowRegime
            );

            const arrowLength =
                maximumArrowLength *
                profileFactor *
                velocityScale;

            /*
             * En las paredes u = 0.
             */
            if (arrowLength > 3) {
                drawArrow(
                    context,
                    arrowStartX,
                    y,
                    arrowLength
                );
            }
        }

        // ---------------------------------------------
        // Perfil envolvente
        // ---------------------------------------------

        /*
         * Esta curva permite distinguir con más claridad
         * la parábola laminar del perfil turbulento plano.
         */
        context.strokeStyle = regimeStyle.color;
        context.lineWidth = 3;

        context.beginPath();

        const profilePoints = 80;

        for (
            let index = 0;
            index <= profilePoints;
            index += 1
        ) {
            const fraction =
                index / profilePoints;

            const y =
                pipeTop +
                fraction * pipeHeight;

            const relativePosition =
                (y - pipeCenterY) /
                Math.max(pipeRadius, 1);

            const profileFactor = getProfileFactor(
                relativePosition,
                flowRegime
            );

            const x =
                arrowStartX +
                maximumArrowLength *
                profileFactor;

            if (index === 0) {
                context.moveTo(x, y);
            } else {
                context.lineTo(x, y);
            }
        }

        context.stroke();

        // ---------------------------------------------
        // Información superior
        // ---------------------------------------------

        context.fillStyle = "#102a33";
        context.font = "16px sans-serif";
        context.textBaseline = "alphabetic";

        context.fillText(
            `D = ${formatNumber(diameter, 3)} m`,
            pipeLeft,
            24
        );

        const velocityText =
            `V media = ${formatNumber(
                velocity,
                3
            )} m/s`;

        const velocityTextWidth =
            context.measureText(velocityText).width;

        context.fillText(
            velocityText,
            pipeRight - velocityTextWidth,
            24
        );

        // ---------------------------------------------
        // Etiqueta inferior del régimen
        // ---------------------------------------------

        context.fillStyle = regimeStyle.color;
        context.font = "bold 16px sans-serif";

        const regimeText =
            `Perfil ${flowRegime.toLowerCase()}`;

        const regimeTextWidth =
            context.measureText(regimeText).width;

        context.fillText(
            regimeText,
            pipeLeft +
                (pipeWidth - regimeTextWidth) / 2,
            canvasHeight - 18
        );

        // ---------------------------------------------
        // Actualización de textos HTML
        // ---------------------------------------------

        if (pipeDiameterValue) {
            pipeDiameterValue.textContent =
                formatNumber(diameter, 3);
        }

        if (velocityProfileLabel) {
            velocityProfileLabel.textContent =
                flowRegime;
        }
    }

    // =====================================================
    // Cálculo hidráulico
    // =====================================================

    function updateSimulation() {
        const diameter = parseNumericValue(
            diameterInput
        );

        const flowRate = parseNumericValue(
            flowRateInput
        );

        const density = parseNumericValue(
            densityInput
        );

        const dynamicViscosity = parseNumericValue(
            viscosityInput
        );

        if (
            Number.isFinite(diameter) &&
            diameterValue
        ) {
            diameterValue.textContent =
                formatNumber(diameter, 3);
        }

        const valuesAreValid =
            Number.isFinite(diameter) &&
            Number.isFinite(flowRate) &&
            Number.isFinite(density) &&
            Number.isFinite(dynamicViscosity) &&
            diameter > 0 &&
            flowRate > 0 &&
            density > 0 &&
            dynamicViscosity > 0;

        if (!valuesAreValid) {
            clearResults();
            return;
        }

        // Área transversal.
        const area =
            Math.PI * Math.pow(diameter, 2) / 4;

        // Velocidad media.
        const velocity = flowRate / area;

        // Número de Reynolds.
        const reynoldsNumber =
            density *
            velocity *
            diameter /
            dynamicViscosity;

        const flowRegime = classifyFlowRegime(
            reynoldsNumber
        );

        if (areaResult) {
            areaResult.textContent =
                formatNumber(area, 6);
        }

        if (velocityResult) {
            velocityResult.textContent =
                formatNumber(velocity, 4);
        }

        if (reynoldsResult) {
            reynoldsResult.textContent =
                formatNumber(reynoldsNumber, 2);
        }

        if (flowRegimeResult) {
            flowRegimeResult.textContent =
                flowRegime;
        }

        drawPipeVisualization(
            diameter,
            velocity,
            flowRegime
        );
    }

    // =====================================================
    // Eventos
    // =====================================================

    const simulationInputs = [
        diameterInput,
        flowRateInput,
        densityInput,
        viscosityInput,
    ];

    simulationInputs.forEach((input) => {
        input.addEventListener(
            "input",
            updateSimulation
        );

        input.addEventListener(
            "change",
            updateSimulation
        );
    });

    // Primera actualización al cargar.
    updateSimulation();
});