// Decision tree definition for the questionnaire.
const decisionTree = {
  q1: {
    text: "Who will handle settlement?",
    options: [
      { label: "Bijlipay handles settlement", next: "q2_model2" },
      { label: "Client handles settlement", next: "q2_model3" }
    ]
  },
  q2_model3: {
    text: "Do you want Bijlipay to deploy devices?",
    options: [
      {
        label: "Yes",
        result: {
          model: "Model 3",
          flow: "Model 3 (TSP) + API + Optional Deployment",
          bullets: [
            "Bijlipay handles device deployment",
            "Captures shop photo and implementation form",
            "Client handles KYC and settlement"
          ]
        }
      },
      {
        label: "No",
        result: {
          model: "Model 3",
          flow: "Model 3 (TSP) + API Only",
          bullets: [
            "Client handles KYC, settlement, and deployment",
            "Bijlipay only provides TID and transactions"
          ]
        }
      }
    ]
  },
  q2_model2: {
    text: "Can you share full merchant data + KYC via API?",
    options: [
      { label: "Yes", next: "q3" },
      { label: "No", next: "q4" }
    ]
  },
  q3: {
    text: "Is your data clean and verified?",
    options: [
      {
        label: "Yes",
        result: {
          model: "Model 2",
          flow: "Model 2 (Aggregator) + Full API Onboarding",
          bullets: [
            "Fastest onboarding",
            "Bijlipay handles KYC, settlement, and deployment"
          ]
        }
      },
      {
        label: "No",
        result: {
          model: "Model 2",
          flow: "Model 2 (Aggregator) + Short Lead API + Bijlipay FOS Completion",
          bullets: [
            "Client shares basic lead",
            "Bijlipay FOS collects full KYC and completes onboarding"
          ]
        }
      }
    ]
  },
  q4: {
    text: "Do you have field sales agents (FOS)?",
    options: [
      {
        label: "No",
        result: {
          model: "Model 2",
          flow: "Model 2 (Aggregator) + Merchant Portal",
          bullets: [
            "Merchant enters data directly",
            "Bijlipay handles KYC, settlement, and deployment"
          ]
        }
      },
      { label: "Yes", next: "q5" }
    ]
  },
  q5: {
    text: "Do you have a backend review team (SAT)?",
    options: [
      {
        label: "Yes",
        result: {
          model: "Model 2",
          flow: "Model 2 (Aggregator) + FOS App + SAT Flow",
          bullets: [
            "FOS collects data",
            "SAT reviews and submits",
            "Bijlipay completes onboarding and deployment"
          ]
        }
      },
      {
        label: "No",
        result: {
          model: "Model 2",
          flow: "Model 2 (Aggregator) + Short Lead API + Bijlipay FOS Completion",
          bullets: []
        }
      }
    ]
  }
};

const contentEl = document.getElementById("content");
const stepIndicatorEl = document.getElementById("stepIndicator");
const progressFillEl = document.getElementById("progressFill");
const restartBtn = document.getElementById("restartBtn");

const MAX_STEPS = 5;
let currentNodeKey = "q1";
let currentStep = 1;

function renderQuestion(nodeKey) {
  const node = decisionTree[nodeKey];
  const optionsHTML = node.options
    .map(
      (option, index) =>
        `<button class="option-btn" data-index="${index}" type="button">${option.label}</button>`
    )
    .join("");

  contentEl.classList.remove("fade-enter");
  contentEl.innerHTML = `
    <div class="fade-enter">
      <h2 class="question">${node.text}</h2>
      <div class="options">${optionsHTML}</div>
    </div>
  `;

  stepIndicatorEl.textContent = `Step ${currentStep} of ${MAX_STEPS}`;
  progressFillEl.style.width = `${(currentStep / MAX_STEPS) * 100}%`;
}

function renderResult(result) {
  const bullets = result.bullets.length
    ? result.bullets.map((item) => `<li>${item}</li>`).join("")
    : "<li>No additional actions beyond this flow.</li>";

  contentEl.classList.remove("fade-enter");
  contentEl.innerHTML = `
    <div class="result-card fade-enter">
      <h2 class="result-title">✅ Recommendation Ready</h2>
      <p><strong>Selected Model:</strong> ${result.model}</p>
      <p class="result-flow">${result.flow}</p>
      <ul class="result-list">${bullets}</ul>
    </div>
  `;

  stepIndicatorEl.textContent = "Completed";
  progressFillEl.style.width = "100%";
}

contentEl.addEventListener("click", (event) => {
  const button = event.target.closest(".option-btn");
  if (!button) return;

  const node = decisionTree[currentNodeKey];
  const selectedOption = node.options[Number(button.dataset.index)];

  if (selectedOption.result) {
    renderResult(selectedOption.result);
    return;
  }

  if (selectedOption.next) {
    currentNodeKey = selectedOption.next;
    currentStep = Math.min(currentStep + 1, MAX_STEPS);
    renderQuestion(currentNodeKey);
  }
});

restartBtn.addEventListener("click", () => {
  currentNodeKey = "q1";
  currentStep = 1;
  renderQuestion(currentNodeKey);
});

renderQuestion(currentNodeKey);
