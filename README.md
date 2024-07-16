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
