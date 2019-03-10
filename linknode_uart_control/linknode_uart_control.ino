int relay0 = 14;
int relay1 = 13;

void setup() {
  Serial.begin(115200);
  pinMode(relay0, OUTPUT);
  pinMode(relay1, OUTPUT);
}

int switch_num = relay0;
void loop() {
  switch(Serial.read()) {
    case '1': switch_num = relay0; break;
    case '2': switch_num = relay1; break;
    case '+': digitalWrite(switch_num, HIGH); break;
    case '-': digitalWrite(switch_num, LOW); break;
    default: break; /* do nothing */
  }
}
