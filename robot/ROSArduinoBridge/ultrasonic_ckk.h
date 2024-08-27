class Ults{
    private:
        int triggerPin;
        int echoPin;
        int delaytime=100;
        int nowtime=millis();
        int valid_time = 50;
        int adapt_num=10;
        double value=0.0;
    public:
        Ults(){}
        void init(const int tr,const int ec){
            triggerPin=tr;
            echoPin=ec;
            pinMode(triggerPin,OUTPUT);
            pinMode(echoPin,INPUT);
        }
        Ults(const int tr,const int ec){
            init(tr, ec);
        }
        void set_adapt_num(int num){
            adapt_num=num;
        }
        void set_delaytime(int t){
            delaytime=t;
        }
        double val(){
            unsigned long duration=0;
            for(int a=0;a<adapt_num;a++){
                // 產生一個10微秒的脈衝以觸發超聲波模塊
                digitalWrite(triggerPin, LOW);
                delayMicroseconds(2);
                digitalWrite(triggerPin, HIGH);
                delayMicroseconds(10);
                digitalWrite(triggerPin, LOW);
                unsigned long messured_num = pulseIn(echoPin, HIGH, 15000);
                if(messured_num == 0){
                  messured_num = 15000;
                }
                duration += messured_num;
                delay(1);
            }
            double out=((double)duration/(double)adapt_num) * 0.034 / 2;
            value=out;
            return out;
        }
        double get_val(){
            if(millis()-nowtime<delaytime){
                return value;
            }else{
                nowtime=millis();
                return val();
            }
        }
};