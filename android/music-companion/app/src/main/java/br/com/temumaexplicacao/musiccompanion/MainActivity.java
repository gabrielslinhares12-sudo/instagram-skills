package br.com.temumaexplicacao.musiccompanion;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.content.Intent;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

public final class MainActivity extends Activity {
    private final Handler handler = new Handler(Looper.getMainLooper());
    private TextView status;
    private final Runnable refresh = new Runnable() {
        @Override public void run() {
            if (status != null) status.setText(MusicAccessibilityService.status());
            handler.postDelayed(this, 900);
        }
    };

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(35, 42, 35, 35);
        TextView title = new TextView(this);
        title.setText("TUE • Música após publicar");
        title.setTextSize(24);
        root.addView(title);
        TextView description = new TextView(this);
        description.setText("\nPost existente: @temumaexplicacao / Halloween\nFaixa aprovada: Thriller — Michael Jackson\n\nO app só atua após seu toque em INICIAR. Não lê senhas, não envia dados à internet e nunca publica novas fotos. A permissão de acessibilidade é opcional e pode ser revogada nas Configurações.\n");
        root.addView(description);
        Button permissions = new Button(this);
        permissions.setText("1. Autorizar acessibilidade (uma vez)");
        permissions.setOnClickListener(v ->
                startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)));
        root.addView(permissions);
        Button start = new Button(this);
        start.setText("2. Iniciar edição de música");
        start.setOnClickListener(v -> {
            if (!MusicAccessibilityService.begin()) {
                status.setText("Habilite primeiro o serviço TUE Música na acessibilidade.");
            }
        });
        root.addView(start);
        Button stop = new Button(this);
        stop.setText("Parar");
        stop.setOnClickListener(v -> MusicAccessibilityService.stop());
        root.addView(stop);
        status = new TextView(this);
        status.setTextSize(16);
        root.addView(status);
        setContentView(root);
    }

    @Override public void onResume() {
        super.onResume();
        handler.removeCallbacks(refresh);
        handler.post(refresh);
    }
    @Override public void onPause() {
        handler.removeCallbacks(refresh);
        super.onPause();
    }
}
