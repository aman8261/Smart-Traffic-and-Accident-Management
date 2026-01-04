// ---------------- PIN SETUP ----------------
int BUZZER = A0;  

int R_TOP = 2;
int Y_TOP = 3;
int G_TOP = 4;

int R_LEFT = 5;
int Y_LEFT = 6;
int G_LEFT = 7;

int R_RIGHT = 8;
int Y_RIGHT = 9;
int G_RIGHT = 10;

int R_BOTTOM = 11;
int Y_BOTTOM = 12;
int G_BOTTOM = 13;

void setup() {
  Serial.begin(9600);
  
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  pinMode(R_TOP, OUTPUT);
  pinMode(Y_TOP, OUTPUT);
  pinMode(G_TOP, OUTPUT);

  pinMode(R_LEFT, OUTPUT);
  pinMode(Y_LEFT, OUTPUT);
  pinMode(G_LEFT, OUTPUT);

  pinMode(R_RIGHT, OUTPUT);
  pinMode(Y_RIGHT, OUTPUT);
  pinMode(G_RIGHT, OUTPUT);

  pinMode(R_BOTTOM, OUTPUT);
  pinMode(Y_BOTTOM, OUTPUT);
  pinMode(G_BOTTOM, OUTPUT);

  allRed();   // Start with all RED
}

// ---------------- BUZZER ----------------
void buzzerOn() {
  digitalWrite(BUZZER, HIGH);
}

void buzzerOff() {
  digitalWrite(BUZZER, LOW);
}

// ---------------- LIGHT CONTROL ----------------
void allRed() {
  digitalWrite(R_TOP, HIGH);
  digitalWrite(Y_TOP, LOW);
  digitalWrite(G_TOP, LOW);

  digitalWrite(R_LEFT, HIGH);
  digitalWrite(Y_LEFT, LOW);
  digitalWrite(G_LEFT, LOW);

  digitalWrite(R_RIGHT, HIGH);
  digitalWrite(Y_RIGHT, LOW);
  digitalWrite(G_RIGHT, LOW);

  digitalWrite(R_BOTTOM, HIGH);
  digitalWrite(Y_BOTTOM, LOW);
  digitalWrite(G_BOTTOM, LOW);
}

void greenTop() {
  allRed();
  digitalWrite(G_TOP, HIGH);
  digitalWrite(R_TOP, LOW);
}

void greenBottom() {
  allRed();
  digitalWrite(G_BOTTOM, HIGH);
  digitalWrite(R_BOTTOM, LOW);
}

void greenLeft() {
  allRed();
  digitalWrite(G_LEFT, HIGH);
  digitalWrite(R_LEFT, LOW);
}
void greenRight() {
  allRed();
  digitalWrite(G_RIGHT, HIGH);
  digitalWrite(R_RIGHT, LOW);
}
// ---------------- MAIN LOOP ----------------
void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "GREEN_TOP")       greenTop();
    else if (cmd == "GREEN_BOTTOM") greenBottom();
    else if (cmd == "GREEN_LEFT") greenLeft();
    else if (cmd == "GREEN_RIGHT") greenRight();
    else if (cmd == "ALL_RED")    allRed();
    else if (cmd == "BUZZER_ON")  buzzerOn();
    else if (cmd == "BUZZER_OFF") buzzerOff();

    Serial.print("Executed: ");
    Serial.println(cmd);
  }
}
