package br.com.temumaexplicacao.musiccompanion;

import android.accessibilityservice.AccessibilityService;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Narrow, explicit one-post UI automation; no network or credential access.
 * Does not assume that selecting a track works until reopened post is checked.
 * Instagram UI versions differ: a missing/ambiguous control stops the action.
 */
public final class MusicAccessibilityService extends AccessibilityService {
    private static final String INSTAGRAM = "com.instagram.android";
    private static final String POST = "https://www.instagram.com/p/DfNVlLDmC8P/";
    private static final String ACCOUNT = "temumaexplicacao";
    private static final String TRACK = "Thriller";
    private static final String ARTIST = "Michael Jackson";
    private static MusicAccessibilityService instance;
    private static String lastStatus = "Aguardando autorização do serviço de acessibilidade.";
    private final Handler handler = new Handler(Looper.getMainLooper());
    private Phase phase = Phase.IDLE;
    private long phaseSince;
    private boolean pending = false;
    private enum Phase {IDLE, POST, MENU, EDIT, MUSIC, SEARCH, RESULTS, TRACK_CHOSEN,
                        EDIT_SAVED, VERIFY, DONE, FAILED}

    public static String status() { return lastStatus; }
    public static boolean begin() {
        if (instance == null) return false;
        instance.startSingleEdit();
        return true;
    }
    public static void stop() {
        if (instance != null) instance.fail("Interrompido pelo proprietário.");
    }

    @Override protected void onServiceConnected() {
        super.onServiceConnected();
        instance = this;
        lastStatus = "Serviço autorizado. Pronto para editar o post escolhido.";
    }
    @Override public void onDestroy() {
        if (instance == this) instance = null;
        handler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }
    @Override public void onInterrupt() { fail("Acessibilidade interrompida."); }
    @Override public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event == null || event.getPackageName() == null ||
                !INSTAGRAM.contentEquals(event.getPackageName())) return;
        schedule(850);
    }

    private void setPhase(Phase next, String message) {
        phase = next;
        phaseSince = android.os.SystemClock.elapsedRealtime();
        lastStatus = message;
        schedule(950);
    }
    private void fail(String why) {
        phase = Phase.FAILED;
        handler.removeCallbacksAndMessages(null);
        pending = false;
        lastStatus = "PARADO: " + why + " Nenhuma republicação foi feita.";
    }
    private void startSingleEdit() {
        handler.removeCallbacksAndMessages(null);
        pending = false;
        setPhase(Phase.POST, "Abrindo o carrossel já publicado...");
        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(POST));
        intent.setPackage(INSTAGRAM);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            startActivity(intent);
        } catch (Exception e) {
            fail("Instagram oficial não instalado ou link indisponível.");
        }
    }
    private void schedule(long ms) {
        if (pending || phase == Phase.IDLE || phase == Phase.DONE || phase == Phase.FAILED) return;
        pending = true;
        handler.postDelayed(() -> {
            pending = false;
            drive();
        }, ms);
    }
    private static String norm(CharSequence s) {
        if (s == null) return "";
        String val = Normalizer.normalize(s, Normalizer.Form.NFD);
        return val.replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT).trim();
    }
    private static String label(AccessibilityNodeInfo n) {
        String t = n.getText() == null ? "" : n.getText().toString();
        String d = n.getContentDescription() == null ? "" : n.getContentDescription().toString();
        return t + " " + d;
    }
    private static void walk(AccessibilityNodeInfo n, List<AccessibilityNodeInfo> results) {
        if (n == null) return;
        results.add(n);
        for (int i = 0; i < n.getChildCount(); i++) walk(n.getChild(i), results);
    }
    private static List<AccessibilityNodeInfo> all(AccessibilityNodeInfo root) {
        List<AccessibilityNodeInfo> nodes = new ArrayList<>();
        walk(root, nodes);
        return nodes;
    }
    private static List<AccessibilityNodeInfo> find(List<AccessibilityNodeInfo> nodes,
                                                     String... values) {
        List<AccessibilityNodeInfo> result = new ArrayList<>();
        for (AccessibilityNodeInfo n : nodes) {
            String text = norm(label(n));
            for (String value : values) {
                if (text.equals(norm(value)) && !result.contains(n)) result.add(n);
            }
        }
        return result;
    }
    private static boolean has(List<AccessibilityNodeInfo> nodes, String text) {
        String wanted = norm(text);
        for (AccessibilityNodeInfo n : nodes) {
            if (norm(label(n)).contains(wanted)) return true;
        }
        return false;
    }
    private boolean tapUnique(List<AccessibilityNodeInfo> nodes, String... names) {
        List<AccessibilityNodeInfo> found = find(nodes, names);
        if (found.size() != 1) return false;
        AccessibilityNodeInfo tap = found.get(0);
        for (int depth = 0; tap != null && depth < 5; depth++, tap = tap.getParent()) {
            if (tap.isClickable()) return tap.performAction(AccessibilityNodeInfo.ACTION_CLICK);
        }
        return false;
    }
    private boolean setUniqueSearch(List<AccessibilityNodeInfo> nodes) {
        List<AccessibilityNodeInfo> editors = new ArrayList<>();
        for (AccessibilityNodeInfo n : nodes) {
            if (n.isEditable() && n.isEnabled()) editors.add(n);
        }
        if (editors.size() != 1) return false;
        Bundle args = new Bundle();
        args.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, TRACK);
        return editors.get(0).performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, args);
    }
    private static boolean inSameRow(AccessibilityNodeInfo track, AccessibilityNodeInfo artist) {
        AccessibilityNodeInfo t = track.getParent();
        AccessibilityNodeInfo a = artist.getParent();
        return t != null && (t == a || t == a.getParent() ||
                (t.getParent() != null && t.getParent() == a.getParent()));
    }
    private boolean selectOriginal(List<AccessibilityNodeInfo> nodes) {
        List<AccessibilityNodeInfo> tracks = find(nodes, TRACK);
        List<AccessibilityNodeInfo> artists = find(nodes, ARTIST);
        if (tracks.size() != 1 || artists.size() != 1 ||
            !inSameRow(tracks.get(0), artists.get(0))) return false;
        AccessibilityNodeInfo t = tracks.get(0);
        for (int i = 0; t != null && i < 5; i++, t = t.getParent()) {
            if (t.isClickable()) return t.performAction(AccessibilityNodeInfo.ACTION_CLICK);
        }
        return false;
    }
    private boolean expired() {
        return android.os.SystemClock.elapsedRealtime() - phaseSince > 25000;
    }
    private void drive() {
        if (phase == Phase.IDLE || phase == Phase.DONE || phase == Phase.FAILED) return;
        if (expired()) { fail("O controle esperado não apareceu na etapa " + phase); return; }
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root == null || root.getPackageName() == null ||
            !INSTAGRAM.contentEquals(root.getPackageName())) { schedule(1200); return; }
        List<AccessibilityNodeInfo> nodes = all(root);
        switch (phase) {
            case POST:
                if (!has(nodes, ACCOUNT)) break;
                if (!has(nodes, "Halloween")) {
                    fail("Não consegui confirmar que o post aberto é o Halloween aprovado.");
                    return;
                }
                if (tapUnique(nodes, "Mais opções", "More options", "Opções", "More")) {
                    setPhase(Phase.MENU, "Procurando a opção Editar...");
                }
                break;
            case MENU:
                if (tapUnique(nodes, "Editar", "Edit")) setPhase(Phase.EDIT, "Editor aberto.");
                break;
            case EDIT:
                if (tapUnique(nodes, "Adicionar música", "Add music")) {
                    setPhase(Phase.MUSIC, "Procurando a biblioteca de música...");
                }
                break;
            case MUSIC:
                if (tapUnique(nodes, "Pesquisar música", "Pesquisar", "Search music", "Search")) {
                    setPhase(Phase.SEARCH, "Inserindo Thriller...");
                }
                break;
            case SEARCH:
                if (setUniqueSearch(nodes)) setPhase(Phase.RESULTS, "Buscando a gravação original...");
                break;
            case RESULTS:
                if (selectOriginal(nodes)) setPhase(Phase.TRACK_CHOSEN, "Faixa original selecionada.");
                break;
            case TRACK_CHOSEN:
                if (tapUnique(nodes, "Concluir", "Done", "Avançar", "Next")) {
                    setPhase(Phase.EDIT_SAVED, "Confirmando edição no Instagram...");
                }
                break;
            case EDIT_SAVED:
                if (tapUnique(nodes, "Concluir", "Done", "Salvar", "Save")) {
                    phase = Phase.VERIFY;
                    phaseSince = android.os.SystemClock.elapsedRealtime();
                    lastStatus = "Reabrindo o mesmo post para verificar áudio...";
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(POST));
                    intent.setPackage(INSTAGRAM);
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);
                    schedule(1800);
                }
                break;
            case VERIFY:
                if (has(nodes, ACCOUNT) && has(nodes, TRACK) && has(nodes, ARTIST)) {
                    phase = Phase.DONE;
                    lastStatus = "Áudio identificado no mesmo post. Confira se a música toca.";
                }
                break;
            default: break;
        }
        schedule(1000);
    }
}
