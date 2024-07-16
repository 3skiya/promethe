# Prometheus Kripto Ticaret Platformu

Bu proje, Binance API'si üzerinden veri çekme, teknik analiz yapma, ticaret stratejileri uygulama, ve tahmin modelleri kullanarak gelecekteki fiyat hareketlerini tahmin etme işlemlerini gerçekleştiren bir kripto ticaret platformudur.

## Kurulum

Gerekli bağımlılıkları yüklemek için:

```bash
pip install -r requirements.txt


Kullanım
Proje klasöründe aşağıdaki Python dosyalarını çalıştırarak farklı fonksiyonları kullanabilirsiniz:

data_fetching.py: Binance API'sine bağlanarak veri çeker ve ilgili API anahtarlarını yükler.
trading_strategies.py: Teknik göstergeler ekler ve dinamik ticaret stratejilerini uygular.
backtesting.py: Backtesting işlemlerini gerçekleştirir ve performans metriklerini hesaplar.
live_simulation.py: Canlı simülasyon işlemlerini gerçekleştirir.
real_trading.py: Gerçek alım satım işlemlerini gerçekleştirir.
summary.py: İşlem listesini ve özet metrikleri oluşturur.
forecasting.py: ARIMA, Prophet ve LSTM tahmin fonksiyonlarını içerir.
performance.py: Performans metriklerini hesaplama ve grafik çizme fonksiyonlarını içerir.
arima_model.py: ARIMA modelini içerir ve ARIMA tahminlerini gerçekleştirir.
prophet_model.py: Prophet modelini içerir ve Prophet tahminlerini gerçekleştirir.
lstm_model.py: LSTM modelini içerir ve LSTM tahminlerini gerçekleştirir.
prometheus.py: Ana dosya. Diğer dosyalardaki fonksiyonları çağırarak veriyi çeker, tahminleri gerçekleştirir, ticaret stratejilerini uygular ve sonuçları özetler.


Yapılandırma
API anahtarlarınızı api.txt dosyasına, ticaret değerlerini TradeValues.txt dosyasına ve model değerlerini ModelValues.txt dosyasına kaydedin.



### Model ve Stratejiler

**Mevcut Modeller:**
1. **Model-1: ARIMA**
   - Zaman serisi tahmin modeli
   - Özellikle kısa vadeli tahminlerde etkilidir

2. **Model-2: LSTM**
   - Derin öğrenme modeli
   - Uzun vadeli bağımlılıkları öğrenebilir

**Ek Modeller ve Stratejiler:**

**iPython Notebook'lar:**
1. **Baseline.ipynb**
2. **BoxPlot.ipynb**
3. **DataCollection.ipynb**
4. **DataProcessor.ipynb**
5. **GAN.ipynb**
6. **LinearRegression.ipynb**
7. **PastSampler.ipynb**
8. **PlotRegularization.ipynb**
9. **PlotTest.ipynb**
10. **Plot_CNN.ipynb**
11. **Plot_GRU.ipynb**
12. **Plot_LSTM.ipynb**

**Python Dosyaları:**
1. **CNN.py**
   - Convolutional Neural Network modeli

2. **GRU.py**
   - Gated Recurrent Unit modeli

3. **GRU_WF.py**
   - Gated Recurrent Unit with Wavelet Transform modeli

4. **LSTM.py**
   - LSTM modeli

5. **Prediction.py**
   - Tahmin fonksiyonları

**Bu modelleri projeye entegre edebilir ve stratejileri genişletebiliriz.**

### Mevcut Tahminler ve Tarihler
**Tahminlerin Tarihleri:**
- Mevcut tahminler 31.12.2023 15:00 - 01.01.2024 00:00 arası

**Nedenleri:**
- `forecast_steps` 10 olarak ayarlanmış, bu nedenle model 10 saatlik tahminler yapar.
- Mevcut tahminler, `start_date` ve `end_date` aralığına dayalı olarak yapılmıştır. 

Bu tarihleri güncelleyerek ve `forecast_steps` değerini değiştirerek daha güncel tahminler elde edebilirsiniz.
